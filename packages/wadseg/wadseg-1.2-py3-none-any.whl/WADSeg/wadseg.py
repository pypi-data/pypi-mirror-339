import torch
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import spacy

def TokenLevel_Attention_Heatmap_ALL_Heads(tokenizer,
                                           model,
                                           device,
                                           
                                           text,
                                           target_layers = [0, 8, 12, 16, 20]
                                           
                                           
                                           ):
  
  def is_lower_triangular(matrix):
    """Check if a matrix is lower triangular."""
    rows, cols = matrix.shape
    for i in range(rows):
        for j in range(i+1, cols):
            if matrix[i, j] != 0:
                return False
    return True
    
# Input text
  inputs = tokenizer(text, return_tensors="pt").to(device)
  
  # Get attention patterns
  with torch.no_grad():
      outputs = model(**inputs, output_attentions=True)
  
  # Extract attention patterns from specified layers
  attentions = outputs.attentions  # Tuple of attention tensors, one for each layer
  
  # Get the number of attention heads
  num_heads = attentions[0].shape[1]
  print(f"Number of attention heads: {num_heads}")
  
  # List to store figures
  figures = []
  
  # Create a figure to display all heads' heatmaps for each layer
  for layer_idx in target_layers:
      # Extract attention for this layer
      layer_attention = attentions[layer_idx].detach().cpu().numpy()[0]  # [num_heads, seq_len, seq_len]
      
      # Calculate grid dimensions
      grid_size = int(np.ceil(np.sqrt(num_heads)))
      
      # Create a figure for this layer
      fig, axes = plt.subplots(grid_size, grid_size, figsize=(15, 15))
      fig.suptitle(f"Layer {layer_idx} - All Attention Heads", fontsize=16)
      
      # Flatten axes for easy indexing
      axes = axes.flatten()
      
      # Plot each attention head
      for head_idx in range(num_heads):
          if head_idx < len(axes):  # Safety check
              # Get attention matrix for this head
              head_attention = layer_attention[head_idx]
              
              # Check if it's lower triangular
              is_lower = is_lower_triangular(head_attention)
              
              # Plot heatmap
              ax = axes[head_idx]
              sns.heatmap(head_attention * 20000, ax=ax, cmap="viridis", cbar=False, vmax=100)
              ax.set_title(f"Head {head_idx}" + (" (Lower Triangular)" if is_lower else ""))
              
              # Remove tick labels for cleaner visualization
              ax.set_xticks([])
              ax.set_yticks([])
              
              # Set equal aspect ratio to make each sub-plot square
              ax.set_aspect('equal', adjustable='box')
      
      # Hide any unused subplots
      for i in range(num_heads, len(axes)):
          axes[i].axis('off')
      
      plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust for the suptitle
      
      # Store the figure instead of showing it
      figures.append(fig)
  
  return figures


def TokenLevel_Attention_Heatmap_Meaning_Heads(tokenizer,
                                           model,
                                           device,
                                           
                                           text,
                                           target_layers = [0, 8, 12, 16, 20]
                                           ):
  
  def is_lower_triangular(matrix):
    """Check if a matrix is lower triangular."""
    rows, cols = matrix.shape
    for i in range(rows):
        for j in range(i+1, cols):
            if matrix[i, j] != 0:
                return False
    return True

  # Input text
  inputs = tokenizer(text, return_tensors="pt").to(device)

  # Get attention patterns
  with torch.no_grad():
      outputs = model(**inputs, output_attentions=True)

  # Extract attention patterns from specified layers

  attentions = outputs.attentions  # Tuple of attention tensors, one for each layer

  # Get the number of attention heads
  num_heads = attentions[0].shape[1]
  print(f"Number of attention heads: {num_heads}")

  # Create a figure to display all heads' heatmaps for each layer
  for layer_idx in target_layers:
      # Extract attention for this layer
      layer_attention = attentions[layer_idx].detach().cpu().numpy()[0]  # [num_heads, seq_len, seq_len]

  # Also create a summary figure with mean attention for each layer
  fig, axes = plt.subplots(len(target_layers), 1, figsize=(6, 6 * len(target_layers)))
  if len(target_layers) == 1:
      axes = [axes]  # Make sure axes is always a list

  # Process each target layer for the summary
  for idx, layer_idx in enumerate(target_layers):
      # Extract attention for this layer
      layer_attention = attentions[layer_idx].detach().cpu().numpy()

      # Mean pooling across attention heads
      mean_attention = np.mean(layer_attention, axis=1)[0]  # Take first batch item
      is_lower = is_lower_triangular(mean_attention)

      # Plot heatmap
      ax = axes[idx]
      sns.heatmap(mean_attention * 20000, ax=ax, cmap="viridis", vmax = 100)

      ax.set_title(f"Layer {layer_idx} Mean Attention Pattern" + (" (Lower Triangular)" if is_lower else ""))
      ax.set_xlabel("Key Tokens")
      ax.set_ylabel("Query Tokens")

      # Set equal aspect ratio to make each sub-plot square
      ax.set_aspect('equal', adjustable='box')

  plt.tight_layout()
  return plt


def Tokens2Sentences(text, tokens, tokenizer, inputs):
    """
    Map tokens to sentences using spaCy.
    
    Args:
        text: Input text
        tokens: List of tokens
        tokenizer: Tokenizer for the model
        inputs: Tokenized inputs
        
    Returns:
        token_sentence_mapping: List mapping each token to its sentence index
        sentences: List of sentences
        sentence_token_indices: Dictionary mapping sentence indices to lists of token indices
    """
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")
    
    # Parse the text with spaCy
    doc = nlp(text)
    sentences = list(doc.sents)
    
    # Get the character spans for each sentence
    sentence_spans = [(sent.start_char, sent.end_char) for sent in sentences]
    
    # Map each token to a sentence
    token_sentence_mapping = []
    
    # Decode each token to get its text representation
    token_texts = []
    for token_id in inputs.input_ids[0].cpu().numpy():
        token_text = tokenizer.decode([token_id]).strip()
        token_texts.append(token_text)
    
    # Find the position of each token in the text
    current_pos = 0
    for token, token_text in zip(tokens, token_texts):
        # Skip special tokens
        if token.startswith('<') and token.endswith('>'):
            token_sentence_mapping.append(-1)
            continue
        
        # Find this token in the text
        if token_text:
            # Look for the token starting from current position
            pos = text.find(token_text, current_pos) if token_text in text[current_pos:] else -1
            
            if pos >= 0:
                # Find which sentence contains this position
                sent_idx = -1
                for i, (start, end) in enumerate(sentence_spans):
                    if start <= pos < end:
                        sent_idx = i
                        break
                
                # If we found a sentence, assign the token to it
                if sent_idx >= 0:
                    token_sentence_mapping.append(sent_idx)
                    current_pos = pos + len(token_text)
                else:
                    # Fallback: assign to the last known sentence
                    token_sentence_mapping.append(token_sentence_mapping[-1] if token_sentence_mapping and token_sentence_mapping[-1] != -1 else 0)
            else:
                # Fallback: assign to the last known sentence
                token_sentence_mapping.append(token_sentence_mapping[-1] if token_sentence_mapping and token_sentence_mapping[-1] != -1 else 0)
        else:
            # For empty tokens, assign to the last known sentence
            token_sentence_mapping.append(token_sentence_mapping[-1] if token_sentence_mapping and token_sentence_mapping[-1] != -1 else 0)
    
    # Create a dictionary mapping sentence indices to lists of token indices
    sentence_token_indices = {}
    for token_idx, sent_idx in enumerate(token_sentence_mapping):
        if sent_idx != -1:  # Skip special tokens
            if sent_idx not in sentence_token_indices:
                sentence_token_indices[sent_idx] = []
            sentence_token_indices[sent_idx].append(token_idx)
    
    return token_sentence_mapping, [sent.text for sent in sentences], sentence_token_indices

def compute_sentence_attention(token_attention, token_sentence_mapping, num_sentences):
    """
    Compute sentence-level attention matrix from token-level attention.
    
    Args:
        token_attention: Token-level attention matrix
        token_sentence_mapping: List mapping each token to its sentence index
        num_sentences: Number of sentences
        
    Returns:
        Sentence-level attention matrix
    """
    sentence_attention = np.zeros((num_sentences, num_sentences))
    sentence_token_counts = np.zeros((num_sentences, num_sentences))
    
    # Sum attention weights between tokens in each sentence pair
    for i, sent_i in enumerate(token_sentence_mapping):
        if sent_i == -1:  # Skip special tokens
            continue
        for j, sent_j in enumerate(token_sentence_mapping):
            if sent_j == -1:  # Skip special tokens
                continue
            sentence_attention[sent_i, sent_j] += token_attention[i, j]
            sentence_token_counts[sent_i, sent_j] += 1
    
    # Average the attention weights
    # Avoid division by zero
    sentence_token_counts = np.maximum(sentence_token_counts, 1)
    sentence_attention = sentence_attention / sentence_token_counts
    
    return sentence_attention

def delta_row(A, i, j):
    """
    Calculate the row difference: A_i,j - A_i-1,j
    
    Args:
        A: Attention matrix
        i: Row index
        j: Column index
        
    Returns:
        Row difference
    """
    if i > 0:
        return A[i, j] - A[i-1, j]
    return A[i, j]  # For the first row, just return the value

def delta_col(A, i, j): 
    """
    Calculate the column difference: A_i,j - A_i,j-1
    
    Args:
        A: Attention matrix
        i: Row index
        j: Column index
        
    Returns:
        Column difference
    """
    if j > 0:
        return A[i, j] - A[i, j-1]
    return A[i, j]  # For the first column, just return the value

def score_1(sentence_attention, i, s_=2):
    """
    Calculate Score1 for sentence i using the formula:
    Score1(i) = -∑(j=i-s_ to i-1) Δrow(Attn, i, j) + ∑(k=i+1 to i+2*s_) Δcol(Attn, k, i)
    
    Args:
        sentence_attention: Sentence-level attention matrix
        i: Sentence index
        s_: Parameter for the range of consideration
        
    Returns:
        Score1 value
    """
    score = 0.0
    num_sentences = sentence_attention.shape[0]
    
    # First term: -∑(j=i-s_ to i-1) Δrow(Attn, i, j)
    for j in range(max(0, i-s_), i):
        score -= delta_row(sentence_attention, i, j)
    
    # Second term: ∑(k=i+1 to i+2*s_) Δcol(Attn, k, i)
    for k in range(i+1, min(i+2*s_+1, num_sentences)):
        score += delta_col(sentence_attention, k, i)
    
    return score

def score_2(sentence_attention, i, s_=2):
    """
    Calculate Score2 for sentence i using the formula:
    Score2(i) = ∑(k=i+1 to i+2*s_) Attn_k,i-1
    
    Args:
        sentence_attention: Sentence-level attention matrix
        i: Sentence index
        s_: Parameter for the range of consideration
        
    Returns:
        Score2 value
    """
    score = 0.0
    num_sentences = sentence_attention.shape[0]
    
    # Check if i-1 is a valid sentence index
    if i <= 0:
        return 0.0
    
    # ∑(k=i+1 to i+2*s_) Attn_k,i-1
    for k in range(i+1, min(i+2*s_+1, num_sentences)):
        score += sentence_attention[k, i-1]
    
    return score

def calculate_sentence_scores(text, tokenizer, model, device, layer_idx, theta=0.5, s_=2):
    """
    Calculate Score1 and Score2 for each sentence in the text.
    
    Args:
        text: Input text
        tokenizer: Tokenizer for the model
        model: The transformer model
        device: Device to run the model on
        layer_idx: Layer index to use for attention
        theta: Weight parameter for Score2
        s_: Parameter for the range of consideration
        
    Returns:
        sentences: List of sentences
        scores: Dictionary with Score1, Score2, and combined Score for each sentence
    """
    # Tokenize the input
    inputs = tokenizer(text, return_tensors="pt").to(device)
    tokens = tokenizer.convert_ids_to_tokens(inputs.input_ids[0])
    
    # Get attention patterns
    with torch.no_grad():
        outputs = model(**inputs, output_attentions=True)
    
    # Extract attention for the specified layer
    token_attention = outputs.attentions[layer_idx].detach().cpu().numpy()
    
    # Mean pooling across attention heads
    mean_token_attention = np.mean(token_attention, axis=1)[0]  # [seq_len, seq_len]
    
    # Map tokens to sentences
    token_sentence_mapping, sentences, _ = Tokens2Sentences(text, tokens, tokenizer, inputs)
    
    # Compute sentence-level attention
    num_sentences = len(sentences)
    sentence_attention = compute_sentence_attention(mean_token_attention, token_sentence_mapping, num_sentences)
    
    # Calculate scores for each sentence
    scores = {}
    for i in range(num_sentences):
        score1 = score_1(sentence_attention, i, s_)
        score2 = score_2(sentence_attention, i, s_)
        combined_score = score1 - theta * score2
        
        scores[i] = {
            'score1': score1,
            'score2': score2,
            'score': combined_score
        }
    
    return sentences, scores, sentence_attention

def SentenceLevel_Attention_Heatmap_Meaning_Heads(sentence_attention, sentences, layer_idx):
    """
    Visualize the sentence-level attention matrices for multiple layers.
    
    Args:
        sentence_attention: List of sentence-level attention matrices
        sentences: List of sentences
        layer_idx: List of layer indices corresponding to the attention matrices
    """
    num_layers = len(sentence_attention)
    fig, axes = plt.subplots(1, num_layers, figsize=(6 * num_layers, 6))
    
    # Handle single layer case
    if num_layers == 1:
        axes = [axes]
    
    for i, attn_matrix in enumerate(sentence_attention):
        ax = axes[i]
        sns.heatmap(attn_matrix*20000, cmap="viridis", vmax=100, ax=ax,
                    xticklabels=[f"S{i+1}" for i in range(len(sentences))], 
                    yticklabels=[f"S{i+1}" for i in range(len(sentences))])
        ax.set_title(f"Layer {layer_idx[i]} Sentence-Level Attention")
        ax.set_xlabel("Key Sentences")
        ax.set_ylabel("Query Sentences")
    
    plt.tight_layout()
    plt.show()

