import numpy as np

# Globals
aa_to_mean = {
 'H': 0.7284397003967741,
 'D': 1.3723602148897058,
 'K': 0.8028853681057971,
 'E': 1.1998145576105261,
 'R': 0.6851662076263159,
 'G': 0.99944564364321,
 'N': 0.8976569004370373,
 'Q': 0.7973146446122222,
 'S': 0.948042795521951,
 'T': 0.7957691674493335,
 'F': 0.6883548022388888,
 'Y': 0.5784814416350001,
 'W': 0.6246138397944446,
 'C': 0.8317935402131148,
 'P': 0.7873109757434782,
 'A': 0.9166398480658536,
 'V': 0.7880105478420454,
 'L': 0.6967138906516854,
 'I': 0.7033991141966293,
 'M': 0.7366778794628865
}

aa_to_std = {
  'C': 0.032019617113087616,
  'S': 0.02470414318883375,
  'A': 0.020021458422232043,
  'G': 0.024034863994747475,
  'T': 0.029743900220318968,
  'V': 0.03268278301247256,
  'N': 0.02329644988941264,
  'Q': 0.024672425740985243,
  'M': 0.022464028849015053,
  'I': 0.019128418301291524,
  'L': 0.02124393473525502,
  'Y': 1e-05,
  'W': 0.021580114674079925,
  'F': 0.020789387332780445,
  'P': 0.02473492675776192,
  'H': 0.020060761621512192,
  'R': 0.02631584431100606,
  'K': 0.03041034805901367,
  'D': 0.042917170495655355,
  'E': 0.03194001848291243
}

window_size = 20
window_indices = np.arange(window_size)
window_function = np.array(-0.00944976 * window_indices**2 + 0.179545 * window_indices + 0.148364, dtype=np.float64)

def get_score(amino_acid, disable_variance=False):
  if disable_variance:
    return aa_to_mean[amino_acid]
  else:
    return np.random.normal(aa_to_mean[amino_acid], aa_to_std[amino_acid])

def predict_current(scores):
    # Compute volume_score and charge_score using numpy dot product
    window_score = np.dot(scores, window_function)
    return window_score

def template_from_sequence(seq, disable_variance=False):
    backwards_sliding_indices = range(len(seq) - window_size, -1, -1)
    scores = [get_score(aa, disable_variance) for aa in seq]
    squiggle = np.array([predict_current(scores[i:i+window_size]) for i in backwards_sliding_indices], dtype=np.float64)
    return squiggle