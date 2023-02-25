# hindi-gpt-mini
This a very small-scale GPT model trained on Munshi Premchand's stories scraped from this [website](http://premchand.co.in/)

Steps to train the model on your own dataset and sample/generate from it are given below:

- Clone the repository
- Place your Hindi dataset in ```input/combined_data.txt```
- Run ```python3 build_vocab.py``` to build the vocabulary
- Finally run ```python3 train.py``` to train the model
- The model will be saved after each step by the name ```model.pth```


The steps to sample from your trained model are:
- Open the ```generate.py``` file and make sure ```load_model``` is set to ```True```
- Then just run ```python3 generate.py``` and your generated text would be in ```hindi.txt```.


The current model is pretty shallow and just trained for 200 epochs, ideally with such a low learning rate a model should be trained for >1000 epochs and a larger depth using greater ```n_heads``` and ```n_layers``` hyperparameter in ```config.py```.
