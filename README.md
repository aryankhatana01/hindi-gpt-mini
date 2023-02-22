# hindi-gpt-mini
This a very small-scale GPT model trained in a very small dataset of Hindi Poems and generates new Poems.
To generate a new poem just run ```python3 generate.py``` and look into ```hindi.txt```.

To train the model on your dataset the replace the content of ```input/combined.txt``` with your data and train the model.

The current model is pretty shallow and just trained for 200 epochs, ideally with such a low learning rate a model should be trained for >1000 epochs and a larger depth using greater ```n_heads``` and ```n_layers``` hyperparameter in ```config.py```.
