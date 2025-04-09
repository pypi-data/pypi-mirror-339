import numpy as np
from b2bTools.general.Io import B2bIo
from b2bTools.singleSeq.constants import DISTRIBUTION_KEYS
from b2bTools.singleSeq.Predictor import MineSuite
from sklearn import mixture


class MineSuiteMSA(MineSuite):

    scriptName = "b2bTools.msaBased.Predictor"

    def predictSeqsFromMSA(self, msaFile, gapCode='-', predTypes=[]):
        # This will read in alignment, should automatically detect format. Code is in general/Io.py
        self.seqAlignments = self.readAlignments(msaFile, resetAlignRefSeqID=True, gapCode=gapCode)

        single_sequences = [(seqId, self.seqAlignments[seqId].replace(gapCode, '')) for seqId in self.seqAlignments.keys()]

        self.predictSeqs(single_sequences, predTypes=predTypes)

        # Now self.allPredictions will give you the predictions for all the individual sequences in the MSA!

    def predictAndMapSeqsFromMSA(self, msaFile, gapCode='-', dataRead=False, predTypes=[]):
        # Read in data only if not yet present - can re-use this function within instance of class if data already present!
        if not dataRead:
            self.predictSeqsFromMSA(msaFile, gapCode=gapCode, predTypes=[*predTypes])

        self.allSeqIds = list(self.seqAlignments.keys())
        self.allSeqIds.sort()

        # All the current prediction types
        prediction_keynames = list(self.allPredictions[self.allSeqIds[0]].keys())

        execution_times = []
        single_values = []

        if 'dynamine_execution_time' in prediction_keynames:
            prediction_keynames.remove('dynamine_execution_time')
            execution_times.append('dynamine_execution_time')

        if 'disomine_execution_time' in prediction_keynames:
            prediction_keynames.remove('disomine_execution_time')
            execution_times.append('disomine_execution_time')

        if 'efoldmine_execution_time' in prediction_keynames:
            prediction_keynames.remove('efoldmine_execution_time')
            execution_times.append('efoldmine_execution_time')

        if 'agmata_execution_time' in prediction_keynames:
            prediction_keynames.remove('agmata_execution_time')
            execution_times.append('agmata_execution_time')

        if 'psper_execution_time' in prediction_keynames:
            prediction_keynames.remove('psper_execution_time')
            execution_times.append('psper_execution_time')

        if 'protein_score' in prediction_keynames:
            prediction_keynames.remove('protein_score')
            single_values.append('protein_score')

        # self.predictionTypes = predictionTypes
        self.prediction_keynames = prediction_keynames
        self.allAlignedPredictions = {}

        sequenceInfo = {}

        for seq_id in self.allSeqIds:
            current_aligned_residues = self.seqAlignments[seq_id]
            current_prediction_values = self.allPredictions[seq_id]

            sequenceInfo[seq_id] = []
            self.allAlignedPredictions[seq_id] = {}

            sequence_residue_index = 0
            for current_aligned_residue in current_aligned_residues:
                sequenceInfo[seq_id].append(current_aligned_residue)
                residues_matching = current_aligned_residue != self.gapCode

                for predictionType in prediction_keynames:
                    if predictionType not in self.allAlignedPredictions[seq_id]:
                        self.allAlignedPredictions[seq_id][predictionType] = []

                    if not residues_matching:
                        self.allAlignedPredictions[seq_id][predictionType].append(None)
                    else:
                        try:
                            current_residue, current_prediction_value, *_other_values = current_prediction_values[predictionType][sequence_residue_index]

                            assert current_residue == current_aligned_residue or current_residue == 'X', f"Amino acid code mismatch in aligned position {sequence_residue_index} (SingleSequence:AlignedSequence) {current_residue}:{current_aligned_residue}"

                            self.allAlignedPredictions[seq_id][predictionType].append(current_prediction_value)
                        except ValueError:
                            import ipdb; ipdb.set_trace()
                            from traceback import print_exc
                            print_exc()

                            raise ValueError(
                                f"Predicted value of type '{predictionType}' not found for input sequence '{seq_id}'")
                        except AssertionError as e:
                            print(self.allAlignedPredictions[seq_id])
                            raise AssertionError(f"{e} in sequence {seq_id}.\nCurrent aligned residues: {''.join(current_aligned_residues)}\nSingle sequence residues: {''.join([residue for residue, _ in current_prediction_values[predictionType]])}")

                if residues_matching:
                    sequence_residue_index += 1

            for single_value in [*single_values, *execution_times]:
                valueFloat = current_prediction_values[single_value]
                self.allAlignedPredictions[seq_id][single_value] = valueFloat

        # self.allAlignedPredictions['sequence'] = sequenceInfo
        self.sequenceInfo = sequenceInfo

    def filterByRefSeq(self, refSeqId):

        assert refSeqId in self.allSeqIds,  'Reference sequence ID {} missing in current prediction information!'.format(
            refSeqId)

        # Here filter so that get back values in reference to the sequence ID that is given.

    def getDistributions(self):
        # Now generate the info for quartiles, ... based on the alignRefSeqID, first entry in alignment file
        self.alignedPredictionDistribs = {}

        # Loop over whole alignment
        alignment_length = len(self.seqAlignments[self.allSeqIds[0]])

        for aligned_residue_index in range(alignment_length):
            for prediction_name in self.prediction_keynames:
                if prediction_name == "viterbi":
                    # Skip viterbi prediction
                    continue

                if prediction_name not in self.alignedPredictionDistribs:
                    self.alignedPredictionDistribs[prediction_name] = {}

                all_prediction_values = [aligned_predictions[prediction_name] for aligned_predictions in self.allAlignedPredictions.values()]
                aligned_column_predicted_values = [prediction_values[aligned_residue_index] for prediction_values in all_prediction_values if prediction_values[aligned_residue_index] is not None]

                # ADRIAN DIAZ: aligned_column_predicted_values can be empty!
                # So, the distribution_info can be a tuple of None values
                distribution_info = self.get_distributions_tuple(aligned_column_predicted_values)

                for distribution_index, distribution_key in enumerate(DISTRIBUTION_KEYS):
                    # import ipdb; ipdb.set_trace()
                    if distribution_key not in self.alignedPredictionDistribs[prediction_name]:
                        self.alignedPredictionDistribs[prediction_name][distribution_key] = []

                    current_distribution_info = distribution_info[distribution_index]
                    self.alignedPredictionDistribs[prediction_name][distribution_key].append(current_distribution_info)

        self.jsonData = B2bIo.getAllPredictionsJson_msa(self, results=self.alignedPredictionDistribs)

        return self.jsonData

    def get_distributions_tuple(self, valueList, outlierConstant=1.5) -> tuple:
        # JR: I put this try-except cause in some MSA we may have only one sequence
        # so the distribution values cannot be calculated

        if not valueList:
            return (None, None, None, None, None)

        try:
            median = np.median(valueList)
            upper_quartile = np.percentile(valueList, 75)
            lower_quartile = np.percentile(valueList, 25)

            IQR = (upper_quartile - lower_quartile) * outlierConstant

            return (median, upper_quartile, lower_quartile, upper_quartile + IQR, lower_quartile - IQR)
        except (IndexError, ValueError):
            return (None, None, None, None, None)

    def getGMMScores(self):
        # predictor_names = [
        #     *constants.DYNAMINE_PREDICTION_NAMES,
        #     *constants.DISOMINE_PREDICTION_NAMES,
        #     *constants.EFOLDMINE_PREDICTION_NAMES,
        #     *constants.AGMATA_PREDICTION_NAMES,
        # ]

        # Collect all biophysical predictions for training using median values from distributions
        training_data = []
        alignment_length = len(
            self.alignedPredictionDistribs[self.prediction_keynames[0]]['median']
        )

        for aln_pos in range(alignment_length):
            # For each alined position
            training_data_current_aligned_position = []
            for pred_type in self.prediction_keynames:
                # For each prediction value
                if pred_type in self.prediction_keynames and pred_type in self.alignedPredictionDistribs:
                    value = self.alignedPredictionDistribs[pred_type]['median'][aln_pos]

                    if value is not None and not np.isnan(value):
                        training_data_current_aligned_position.append(value)

            if len(training_data_current_aligned_position) == len(self.prediction_keynames):
                training_data.append(training_data_current_aligned_position)

        # import ipdb; ipdb.set_trace()
        # Stack the values for training
        X_train = np.vstack(training_data)

        # Initialize GMM classifier
        gmm_classifier = mixture.GaussianMixture(n_components=1, covariance_type="full", verbose=3, verbose_interval=1)

        # Fit GMM
        gmm_classifier.fit(X_train)

        # Calculate scores for each sequence
        self.GMMScores = {}
        for seq_id in self.allSeqIds:
            sequence_gmm_scores = []

            for aln_pos in range(alignment_length):
                current_position_values = []
                for pred_type in self.prediction_keynames:
                    if pred_type in self.allAlignedPredictions[seq_id]:
                        value = self.allAlignedPredictions[seq_id][pred_type][aln_pos]

                        if value is not None and not np.isnan(value):
                            current_position_values.append(value)

                if current_position_values:
                    # Reshape to match training data format (1, n_features)
                    X = np.array(current_position_values).reshape(1, -1)
                    scores = gmm_classifier.score_samples(X)
                    sequence_gmm_scores.extend(scores.tolist())

            self.GMMScores[seq_id] = sequence_gmm_scores

        return self.GMMScores

    def getCutoffResidues(self):
        """
        Identifies residues that are over the 95, 99 and 99.9 percentiles as estimated by the GMM using the median of the predictions.
        Stores results in self.cutoffResidues dictionary.
        """
        if not hasattr(self, 'GMMScores'):
            self.getGMMScores()

        # Collect all scores to calculate percentiles
        all_scores = []
        for seq_id in self.GMMScores:
            all_scores.extend(self.GMMScores[seq_id])

        # Calculate percentile cutoffs
        cutoff_95 = np.percentile(all_scores, 95)
        cutoff_99 = np.percentile(all_scores, 99)
        cutoff_99_9 = np.percentile(all_scores, 99.9)

        # Store cutoff residues for each sequence
        self.cutoffResidues = {}
        for seq_id in self.GMMScores:
            scores = self.GMMScores[seq_id]
            residue_indexes_99_9 = [i for i, score in enumerate(scores) if score > cutoff_99_9]
            residue_indexes_99 = [i for i, score in enumerate(scores) if score > cutoff_99 and i not in residue_indexes_99_9]
            residue_indexes_95 = [i for i, score in enumerate(scores) if score > cutoff_95 and i not in residue_indexes_99 and i not in residue_indexes_99_9]

            self.cutoffResidues[seq_id] = {
                'res99_9': residue_indexes_99_9,
                'res99': residue_indexes_99,
                'res95': residue_indexes_95,
            }

        return self.cutoffResidues
