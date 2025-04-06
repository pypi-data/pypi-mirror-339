from .print_fonts import PrintFonts

class DeepLearning():
    def help(self):
        """Get all methods with descriptions"""
        pf = PrintFonts()
        text = """
        ## DEEP LEARNING HELP
        ! Here you can find everything i've studied about Deep Learning, with Tensorflow Keras
        
        # Imports:  
        -imports(): Common imports for Keras
        
        # Approach
        -common_path(): Simple step-by-step schema when dealing with Deep Learning 
        
        # Layers:
        -dense(): A densely connected network is a pile of Dense layers to elaborate vector data. 
        -convnet(): Convolutions layers search local patterns, applying the same transformation to different (patch).
        -rnn(): Recurrent Neural Network elaborates a single timestep input at time while keeping a state.

        # Pre-elaboration data techniques:
        -pre_elaboration(): List the most used data pre-elaboration techniques
        
        # Advanced techniques:
        -callbacks(): Explain how to configure Keras Callbacks for different advanced techniques
        -dropout(): Explain how to set a simple DropOut
        -learning_rate_scheduler(): Explain how to modify learning rate based on epochs
        -mixed_precision(): Explain how to setup a mixed_precision training
        -gradient_accumulation(): Explain how to use gradient accolumation to increase batch size
        
        # Model visualizzation: 
        -TensorBoard(): Show how to use Tensorflow TensorBoard to gain insights of your neural network
        -plot_model(): Show how to use Keras plot_model to create an image of the layers of your neural network
        
        # Ultimating the model
        -compile(): Explain how to compile a model
        -train(): Explain how to train a model
        -train_with_gradient_accumulation(): Explain advanced techniques for training a model
        -predict_regression(): Explain how to make regression predictions with the model
        -predict_classification(): Explain how to make classification predictions with the model
        -evaluate(): Explain how to evaluate the model
        
        # Plot results
        -plot(): Explain how to plot results of the model
        """
        pf.format(text)


    def imports(self):
        pf = PrintFonts()
        text = """
        ## COMMON IMPORTS FOR KERAS
        
        from keras import models
        from keras import layers
        """
        pf.format(text)


    def common_path(self):
        pf = PrintFonts()
        text = """
         ## SIMPLE STEP BY STEP MENTAL SCHEMA TO WORK WITH DEEP LEARNING

        ! Define problem and create/find dataset
        ! Select the evaluation param (example: accuracy or roc auc curve..)
        ! Find an evaluation protocol
        ! Prepare data
        ! Create a model that performs better than a random one
        ! Create a model that does Overfit
        ! Regularize the model and optimize hyperparams
        ! Test your model
         """
        pf.format(text)

    def pre_elaboration(self):
        pf = PrintFonts()
        text = """
        ## FOR LABELS (target): 
        ! to_categorical() = Single-label Classification - Requires: categorical_crossentropy
        ! Integer encoding = Single-label Classification - Requires: sparse_categorical_crossentropy
        ! Multi-hot encoding = Multi-label Classification -	Similar as to_categorical, but more active classes
        ! LabelEncoder (sklearn) = Prepare labels as integers - Often used before other transformations
        
        ! Example:
        ## to_categorical()
        ! to_categorical is a pre-elaboration data method used to convert int labels in one-hot encoding 
        ! one-hot encoding is the required format for single-label classification networks.
        
        ! When to use:
        ! When you have int labels and the model uses:
        ! activation='softmax' in the output layer
        ! loss='categorical_crossentropy'
        ! If instead it uses sparse_categorical_crossentropy, you can avoid using to_categorical.
        
        from keras.utils import to_categorical

        labels = [0, 2, 1]
        one_hot_labels = to_categorical(labels)
        
        ! Output:
        ! array([[1., 0., 0.],
        !        [0., 0., 1.],
        !        [0., 1., 0.]])
        
        
        ## FOR NUMERICAL FEATURES:
        ! Normalization	= Transform values in [0, 1] - When: data have known range
        ! Standardization (Z-score) = Mean: 0, std_dev: 1 - When: gaussian data
        ! MinMaxScaler (sklearn) = Similar to Normalization	- Ideal for sigmoid layer
        ! RobustScaler = Use median and IQR - When: there are outliers
        
        ! Example:
        ## MinMaxScaler()
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)
        
        
        ## CATEGORICAL FEATURES (input)
        ! One-Hot Encoding = One column for category - When: Few distinct values
        ! Label Encoding = Integers as categories - When: Non numerical values
        ! Embedding Layer = Map categories into vectors - When: Many categories (example: words)
        ! Binary Encoding = Binary encoding - When: Many categories (for ML)
        
        
        ## FOR TEXT
        ! Tokenization = Divide text into words
        ! Padding/Truncation = Make every sentences of the same length
        ! Text vectorization = Transform words into numbers
        ! Word Embeddings = Transforms words into numerical vectors
        ! TF-IDF = Weight words in base of their frequency
        
        
        ## FOR IMAGES
        ! Rescaling (es. /255) = Transform pixels into [0, 1]
        ! Resize / crop / pad = Make every image of the same dimension
        ! Data augmentation	= Adds "new" images changing variability (examples: flip, rotate, ecc.)
        
        
        ## GENERAL RULES:
        ! Numerical data = Normalize or Standarize
        ! Categorical data = One-hot or embedding
        ! Text = Tokenize or Embedding
        ! Images = Rescaling or Augmenting
        ! Labels = to_categorical or Encoding Multilabel
        """
        pf.format(text)


    def dense(self):
        pf = PrintFonts()
        text = """
        ## DENSELY CONNECTED NETWORKS (DENSE)
        ! A densely connected network is a pile of Dense layers to elaborate vector data. 
        ! This network doesn't have any specific structure in its input architecture: 
        ! every layers if fully connected with the others.

        ## CLASSIFICATION - BINARY
        from keras import models
        from keras import layers

        model = models.Sequential()
        model.add(layers.Dense(32, activation='relu', input_shape=(num_input_features, )))
        model.add(layers.Dense(32, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))
        
        model.compile(optimizer='rmsprop', loss='binary_crossentropy')


        ## CLASSIFICATION - SINGLE-LABEL
        from keras import models
        from keras import layers
        
        model = models.Sequential()
        model.add(layers.Dense(32, activation='relu', input_shape=(num_input_features, )))
        model.add(layers.Dense(32, activation='relu'))
        model.add(layers.Dense(num_classes, activation='softmax'))
        
        model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
        ! If int you can use loss='sparse_categorical_crossentropy' instead


        ## CLASSIFICATION - MULTI-LABEL
        from keras import models
        from keras import layers
        
        model = models.Sequential()
        model.add(layers.Dense(32, activation='relu', input_shape=(num_input_features, )))
        model.add(layers.Dense(32, activation='relu'))
        model.add(layers.Dense(num_classes, activation='sigmoid'))
        
        model.compile(optimizer='rmsprop', loss='binary_crossentropy')

        
        ## REGRESSION - CONTINUOUS VALUES
        from keras import models
        from keras import layers
        
        model = models.Sequential()
        model.add(layers.Dense(32, activation='relu', input_shape=(num_input_features, )))
        model.add(layers.Dense(32, activation='relu'))
        model.add(layers.Dense(num_classes))
        
        model.compile(optimizer='rmsprop', loss='mse')
        ! You can use MSE or MAE or other metrics
        """
        pf.format(text)


    def convnet(self):
        pf = PrintFonts()
        text = """
        ! Convolutions layers search local patterns from spacial point-of-view, 
        ! applying the same transformation to different spatial positions (patch).
    
        ! This network is very effective in data elaboration and modularity. 
        ! Conv1D: useful for sequences (like text)
        ! Conv2D: useful for images
        ! Conv3D: useful for volumes (like videos)
        
        ! These networks must use Pooling layer(s) to sub-sample the data (and reduce their size)
        ! and usually they end with Dense layer(s) and before them a Flatten() layer of a GlobalAveragePooling() layer.

        ! However, these networks are replaced by Depth Separable Convolution layers (SeparableConv2D) 
        ! this is faster and more efficient.
        
        
        ## CONV - IMAGE CLASSIFICATION
        from keras import models
        from keras import layers
        
        model = models.Sequential()
        model.add(layers.SeparableConv2D(32, 3, activation='relu', input_shape=(height, width, channels)))
        model.add(layers.SeparableConv2D(64, 3, activation='relu'))
        model.add(layers.MaxPooling2D(2))
        model.add(layers.SeparableConv2D(64, 3, activation='relu'))
        model.add(layers.SeparableConv2D(128, 3, activation='relu'))
        model.add(layers.GlobalAveragePooling2D())  
        model.add(layers.Dense(32, activation='relu'))
        model.add(layers.Dense(num_classes, activation='softmax'))
        
        model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
        
        ! You may use Flatten() instead of GlobalAveragePooling2D()
        """
        pf.format(text)

    def rnn(self):
        pf = PrintFonts()
        text = """
        ! Recurrent Neural Network elaborates a single timestep input at time while keeping a state
        ! (a vector or list of vectors, a point in the states-space)
        ! This network performs better than Conv1D for time-series when recent-past is more important than long-past.
        
        ! There are three possible RNN layers in Keras:
        ! SimpleRNN: the simplest RNN
        ! LSTM: the strongest RNN, but slower
        ! GRU: a simpler LSTM and less expensive
        
        
        ## BINARY CLASSIFICATION FOR VECTOR SEQUENCES - LSTM
        from keras import models
        from keras import layers
        
        model = models.Sequential()
        model.add(layers.LSTM(32, return_sequences=True, input_shape=(num_timesteps, num_features)))
        model.add(layers.LSTM(32, return_sequences=True))
        model.add(layers.LSTM(32))
        model.add(layers.Dense(num_classes, activation='sigmoid'))
        
        model.compile(optimizer='rmsprop', loss='binary_crossentropy')
        """
        pf.format(text)


    def callbacks(self):
        pf = PrintFonts()
        text = """
        ## CREATE CALLBACKS FUNCTIONS TO CONFIGURE DIFFERENT ADVANCED TECHNIQUES
        
        ! You can use Keras callbacks methods to customize and gain insight of what's happening in your neural network.

        ## ModelCheckpoint and EarlyStopping
        ! EarlyStopping: stop the training when a certain condition or loss is met
        ! ModelCheckpoint: save the model when a certain condition is met</li>

        import keras
        
        callbacks_list = [
            keras.callbacks.EarlyStopping(monitor='acc', patience=1),
            keras.callbacks.ModelCheckpoint(filepath='my_model.h5', monitor='val_loss', save_best_only=True)
        ]
        
        model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
        model.fit(x, y, epochs=10, callbacks=callbacks_list, validation_data=(x_val, y_val))


        ! You can create your own Callback method.
        ! These are some keras.callbacks.Callback methods already present in Keras:
        ! on_epoch_begin 
        ! on_epoch_end
        ! on_batch_begin
        ! on_batch_end
        ! on_train_begin
        ! on_train_end
        """
        pf.format(text)

    def dropout(self):
        pf = PrintFonts()
        text = """
        ## USE DROPOUT

        model = keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=[1]),
            layers.Dropout(0.2),  # Dropout layer
            layers.Dense(1)
        ])

        # Add a hidden layer with Dropout to prevent overfitting.
        # PS: This can be used with every kind of model
        """
        pf.format(text)


    def learning_rate_scheduler(self):
        pf = PrintFonts()
        text = """
        ## LEARNING RATE SCHEDULER

        # A learning rate scheduler adjusts the learning rate during training based on the current epoch.
        
        def lr_scheduler(epoch, lr):
            if epoch < 10:
                return lr
            else:
                return lr * tf.math.exp(-0.1)  # Reduce learning rate exponentially after epoch 10
        
        # Create a learning rate scheduler callback
        lr_callback = tf.keras.callbacks.LearningRateScheduler(lr_scheduler)
        """
        pf.format(text)


    def mixed_precision(self):
        pf = PrintFonts()
        text = """
        ## MIXED PRECISION

        # Mixed precision training uses lower precision (e.g., float16) to speed up training and reduce memory usage.

        # Enable mixed precision in TensorFlow
        from tensorflow.keras.mixed_precision import set_global_policy
        set_global_policy("mixed_float16")  # Set the global policy to mixed precision
        """
        pf.format(text)


    def gradient_accumulation(self):
        pf = PrintFonts()
        text = """
        ## GRADIENT ACCUMULATION

        # Gradient accumulation allows us to simulate larger batch size by accumulating gradients over multiple batches.

        class GradientAccumulator:
            def __init__(self, accum_steps):
                self.accum_steps = accum_steps
                self.accum_gradients = None
        
            def accumulate_gradients(self, gradients):
                if self.accum_gradients is None:
                    self.accum_gradients = [tf.zeros_like(g) for g in gradients]
                for i in range(len(gradients)):
                    self.accum_gradients[i] += gradients[i]
        
            def apply_gradients(self, optimizer, model):
                optimizer.apply_gradients(zip(self.accum_gradients, model.trainable_variables))
                self.accum_gradients = None  # Reset accumulated gradients
        
        # Initialize the gradient accumulator
        accum_steps = 4  # Accumulate gradients over 4 batches
        gradient_accumulator = GradientAccumulator(accum_steps)
        """
        pf.format(text)


    def compile(self):
        pf = PrintFonts()
        text = """
        ## COMPILE THE MODEL

        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

        # optimizer: Algorithm used to update the model's weights during training (e.g., Adam, SGD).
        # loss: Function that measures the error between the model's predictions and the true values. 
                # For regression, common choices include 'mean_squared_error' or 'mean_absolute_error'.
        # metrics: List of metrics to evaluate the model's performance during training and testing.
        """
        pf.format(text)


    def train(self):
        pf = PrintFonts()
        text = """
        ## TRAIN THE MODEL

        history = model.fit(x_train, y_train, epochs=100, batch_size=32, callbacks=callbacks_list)

        # epochs: Number of times the entire dataset is passed through the model during training.
        # batch_size: Number of samples processed before the model's weights are updated.
        # callbacks: Callback function(s) to use in your model (check callbacks() for more info)
        """
        pf.format(text)


    def train_with_gradient_accumulation(self):
        pf = PrintFonts()
        text = """
        ## TRAIN THE MODEL WITH GRADIENT ACCUMULATION

        # Custom training loop with gradient accumulation
        def train_with_gradient_accumulation(model, dataset, epochs, accum_steps):
            for epoch in range(epochs):
                print(f"Epoch {epoch + 1}/{epochs}")
                for step, (x_batch, y_batch) in enumerate(dataset):
                    with tf.GradientTape() as tape:
                        predictions = model(x_batch, training=True)
                        loss = model.compute_loss(y_batch, predictions)
                    gradients = tape.gradient(loss, model.trainable_variables)
                    gradient_accumulator.accumulate_gradients(gradients)
        
                    # Apply gradients after accumulating over `accum_steps` batches
                    if (step + 1) % accum_steps == 0:
                        gradient_accumulator.apply_gradients(model.optimizer, model)
        
        # Prepare the dataset for training
        batch_size = 64
        train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(batch_size)
        
        # Train the model
        epochs = 20
        train_with_gradient_accumulation(model, train_dataset, epochs, accum_steps)
        """
        pf.format(text)


    def predict_regression(self):
        pf = PrintFonts()
        text = """
        ## MAKE REGRESSION PREDICTIONS WITH THE MODEL

        y_pred = model.predict(x_test)

        # Use the trained model to predict values for new input data.
        """
        pf.format(text)


    def predict_classification(self):
        pf = PrintFonts()
        text = """
        ## MAKE CLASSIFICATION PREDICTIONS WITH THE MODEL

        # Make predictions on the test set
        y_pred = model.predict(x_test)
        y_pred_labels = np.argmax(y_pred, axis=1)
        y_true_labels = np.argmax(y_test, axis=1)

        # Plot some examples
        class_names = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
        
        plt.figure(figsize=(15, 10))
        for i in range(10):
            plt.subplot(2, 5, i + 1)
            plt.imshow(x_test[i])
            plt.title(f"True: {class_names[y_true_labels[i]]}\nPred: {class_names[y_pred_labels[i]]}")
            plt.axis("off")
        plt.tight_layout()
        plt.show()
        """
        pf.format(text)


    def evaluate(self):
        pf = PrintFonts()
        text = """
        ## EVALUATE THE MODEL

        test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
        print(f"Test Loss: {test_loss:.4f}")
        print(f"Test Accuracy: {test_accuracy:.4f}")

        # Evaluate the model on the test set and plot the training history.
        """
        pf.format(text)

    def TensorBoard(self):
        pf = PrintFonts()
        text = """
        ## CREATE WEBSITE WITH INSIGHTS OF YOUR NEURAL NETWORK

        import keras

        callbacks_list = [
            keras.callbacks.TensorBoard(log_dir='my_log_dir', histogram_freq=1, embeddings_freq=1)
        ]
        
        model.fit(x, y, epochs=20, batch_size=128, validation_split=0.2, callbacks=callbacks_list)
        """
        pf.format(text)

    def plot_model(self):
        pf = PrintFonts()
        text = """
        ## CREATE IMAGE OF THE LAYERS OF YOUR NEURAL NETWORK

        from keras.utils import plot_model
        
        plot_model(model, show_shapes=True, to_file='model.png')
        """
        pf.format(text)


    def plot(self):
        pf = PrintFonts()
        text = """
        ## MAKE PREDICTIONS WITH THE MODEL

        plt.scatter(x_train, y_train, label='Training Data')
        plt.plot(x_test, y_pred, color='red', label='Predictions')
        plt.legend()
        plt.show()

        # Visualize the training data, predictions, and the learned regression line.
        """
        pf.format(text)