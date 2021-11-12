HARD = 1
MEDIUM = 0.75
EASY = 0.5

# Format: frame: (# of objects visible, difficulty multiplier)
answers = {
  "CC 2015-CC_2_18-126-6.633": (2, HARD),
  "CC 2015-CC_2_18-126-6.667": (2, HARD),
  "CC 2015-CC_2_18-126-6.700": (2, HARD),
  "CC 2015-CC_2_18-126-6.733": (2, HARD),
  "CC 2015-CC_2_18-126-6.767": (2, HARD),
  "CC 2015-CC_2_18-126-6.800": (2, HARD),
  "CC 2015-CC_2_18-126-6.833": (2, HARD),
  "CC 2015-CC_2_18-126-6.867": (2, HARD),
  "CC 2015-CC_2_18-126-6.900": (2, HARD),
  "CC 2015-CC_2_18-126-6.933": (2, HARD),

  "SA 2017-CC_7_06-69-62.433": (6, MEDIUM),
  "SA 2017-CC_7_06-69-62.467": (5, MEDIUM),
  "SA 2017-CC_7_06-69-62.500": (5, MEDIUM),
  "SA 2017-CC_7_06-69-62.533": (5, MEDIUM),
  "SA 2017-CC_7_06-69-62.567": (5, MEDIUM),
  "SA 2017-CC_7_06-69-62.600": (5, MEDIUM),
  "SA 2017-CC_7_06-69-62.633": (5, MEDIUM),
  "SA 2017-CC_7_06-69-62.667": (5, MEDIUM),
  "SA 2017-CC_7_06-69-62.700": (5, MEDIUM),
  "SA 2017-CC_7_06-69-62.733": (5, MEDIUM),

  "CA 2017-TOM_CC0705_20171015-6-557.033": (2, HARD),
  "CA 2017-TOM_CC0705_20171015-6-557.067": (2, HARD),
  "CA 2017-TOM_CC0705_20171015-6-557.100": (2, HARD),
  "CA 2017-TOM_CC0705_20171015-6-557.133": (2, HARD),
  "CA 2017-TOM_CC0705_20171015-6-557.167": (2, HARD),
  "CA 2017-TOM_CC0705_20171015-6-557.200": (2, HARD),
  "CA 2017-TOM_CC0705_20171015-6-557.233": (2, HARD),
  "CA 2017-TOM_CC0705_20171015-6-557.267": (2, HARD),
  "CA 2017-TOM_CC0705_20171015-6-557.300": (0, HARD),
  "CA 2017-TOM_CC0705_20171015-6-557.333": (0, HARD),

  "CA 2017-TOM_CC0705_20171015-24-210.033": (1, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-24-210.067": (1, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-24-210.100": (1, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-24-210.133": (1, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-24-210.167": (1, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-24-210.200": (1, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-24-210.233": (1, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-24-210.267": (1, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-24-210.300": (1, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-24-210.333": (1, MEDIUM),

  "SA 2017-CC_7_06-200-60.433": (1, EASY),
  "SA 2017-CC_7_06-200-60.467": (1, EASY),
  "SA 2017-CC_7_06-200-60.500": (1, EASY),
  "SA 2017-CC_7_06-200-60.533": (1, EASY),
  "SA 2017-CC_7_06-200-60.567": (1, EASY),
  "SA 2017-CC_7_06-200-60.600": (1, EASY),
  "SA 2017-CC_7_06-200-60.633": (1, EASY),
  "SA 2017-CC_7_06-200-60.667": (1, EASY),
  "SA 2017-CC_7_06-200-60.700": (1, EASY),
  "SA 2017-CC_7_06-200-60.733": (1, EASY),

  "SA 2017-CC_7_06-201-15.433": (0, EASY),
  "SA 2017-CC_7_06-201-15.467": (0, EASY),
  "SA 2017-CC_7_06-201-15.500": (0, EASY),
  "SA 2017-CC_7_06-201-15.533": (0, EASY),
  "SA 2017-CC_7_06-201-15.567": (0, EASY),
  "SA 2017-CC_7_06-201-15.600": (0, EASY),
  "SA 2017-CC_7_06-201-15.633": (0, EASY),
  "SA 2017-CC_7_06-201-15.667": (0, EASY),
  "SA 2017-CC_7_06-201-15.700": (0, EASY),
  "SA 2017-CC_7_06-201-15.733": (0, EASY),

  "CA 2017-TOM_CC0705_20171015-5-350.233": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-5-350.267": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-5-350.300": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-5-350.333": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-5-350.367": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-5-350.400": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-5-350.433": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-5-350.467": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-5-350.500": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-5-350.533": (0, MEDIUM),

  "CA 2017-TOM_CC0705_20171015-4-452.233": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-4-452.267": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-4-452.300": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-4-452.333": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-4-452.367": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-4-452.400": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-4-452.433": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-4-452.467": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-4-452.500": (0, MEDIUM),
  "CA 2017-TOM_CC0705_20171015-4-452.533": (0, MEDIUM),
}

class Scorer:
  """
  An object to track scoring state.
  "Positive" refers to a frame with an event.
  "Negative" refers to a frame without an event.
  """
  def __init__(self):
    self.false_positive_count = 0 # number of frames where a frame was flagged as having an object, when it in fact did not
    self.false_negative_count = 0 # number of frames where a frame was flagged as not having an object, when in fact it did
    self.num_perfectly_correct_positives = 0 # number of frames where a frame with object(s) was perfectly identified
    self.num_perfectly_correct_negatives = 0 # number of frames where a frame without an object was perfectly identified
    self.num_kinda_correct_positives = 0
    self.positives_score = 0
    self.negatives_score = 0
    self.total_possible_positives_score = 0
    self.total_possible_negatives_score = 0
    self.positive_total_count = 0 # number of frames processed with an object
    self.negative_total_count = 0 # number of frames processed without an object

  def score_frame(self, frame_name, num_blobs_found):
    if frame_name in answers:
      correct_num_fish, difficulty_multiplier = answers[frame_name]
      
      if correct_num_fish == 0:
        self.negative_total_count += 1
        self.total_possible_negatives_score += difficulty_multiplier
        if num_blobs_found == 0:
          self.num_perfectly_correct_negatives += 1
          self.negatives_score += difficulty_multiplier
        else:
          self.false_positive_count += 1
      elif correct_num_fish > 0:
        self.positive_total_count += 1
        self.total_possible_positives_score += difficulty_multiplier
        if num_blobs_found == 0:
          self.false_negative_count += 1
        elif correct_num_fish == num_blobs_found:
          self.num_perfectly_correct_positives += 1
          self.positives_score += difficulty_multiplier
        else:
          self.num_kinda_correct_positives += 1
          # Give partial credit proportional to how close it was to the right answer
          # Only 1 off = full credit, 2 off = half credit, 3 off = 1/3 credit, etc.
          self.positives_score += difficulty_multiplier*(1/abs(correct_num_fish-num_blobs_found))
    else:
      print("Warning: frame did not have associated answer.")
        
  def print_results(self):
    print("\nRESULTS:\n"
    f"Num Positives Correct: {self.num_perfectly_correct_positives} out of {self.positive_total_count} "
    f"({'%.2f'%(self.num_perfectly_correct_positives*100/self.positive_total_count)}%)\n"
    f"Num Positives Kind Of Correct: {self.num_kinda_correct_positives} out of {self.positive_total_count} "
    f"({'%.2f'%(self.num_kinda_correct_positives*100/self.positive_total_count)}%)\n"
    f"Missed Positives (False Negatives): {self.false_negative_count} out of {self.positive_total_count} "
    f"({'%.2f'%(self.false_negative_count*100/self.positive_total_count)}%)\n"
    f"Num Negatives Correct: {self.num_perfectly_correct_negatives} out of {self.negative_total_count} "
    f"({'%.2f'%(self.num_perfectly_correct_negatives*100/self.negative_total_count)}%)\n"
    f"Missed Negatives (False Positives): {self.false_positive_count} out of {self.negative_total_count} "
    f"({'%.2f'%(self.false_positive_count*100/self.negative_total_count)}%)\n"
    "---------\n"
    f"Positive score: {'-' if self.positive_total_count == 0 else '%.2f'%(self.positives_score*100/self.total_possible_positives_score)}%\n"
    f"Negative score: {'-' if self.negative_total_count == 0 else '%.2f'%(self.negatives_score*100/self.total_possible_negatives_score)}%\n")
