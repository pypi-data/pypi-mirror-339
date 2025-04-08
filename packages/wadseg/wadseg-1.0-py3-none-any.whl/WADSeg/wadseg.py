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


