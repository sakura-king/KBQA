# coding=utf-8
import keras
from bilstm_crf_model import BiLstmCrfModel
from data_helpers import NerDataProcessor
import tensorflow as tf

max_len = 80
vocab_size = 2418
embedding_dim = 200
lstm_units = 128

if __name__ == '__main__':
    ndp = NerDataProcessor(max_len, vocab_size)
    train_X, train_y = ndp.read_data(
            path="../ChineseBLUE/cMedQANER/train.txt",
            is_training_data=True
        )
    train_X, train_y = ndp.encode(train_X, train_y)
    dev_X, dev_y = ndp.read_data(
            "../ChineseBLUE/cMedQANER/dev.txt",
            is_training_data=False
        )
    dev_X, dev_y = ndp.encode(dev_X, dev_y)
    test_X, test_y = ndp.read_data(
            "../ChineseBLUE/cMedQANER/test.txt",
            is_training_data=False
        )
    test_X, test_y = ndp.encode(test_X, test_y)
    with tf.compat.v1.Session() as sess:
        class_nums = ndp.class_nums
        word2id = ndp.word2id
        tag2id = ndp.tag2id
        id2tag = ndp.id2tag
        import pickle
        pickle.dump(
                (word2id, tag2id, id2tag),
                open("./checkpoint/word_tag_id.pkl", "wb")
            )

        bilstm_crf = BiLstmCrfModel(
                max_len,
                vocab_size,
                embedding_dim,
                lstm_units,
                class_nums
            )
        model = bilstm_crf.build()
        
        reduce_lr = keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=4,
            verbose=1)

        earlystop = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            verbose=2,
            mode='min'
            )
        best_model_filepath = './checkpoint/best_bilstm_crf_model.h5'
        checkpoint = keras.callbacks.ModelCheckpoint(
            best_model_filepath,
            monitor='val_loss',
            verbose=1,
            save_best_only=True,
            mode='min'
            )
        model.fit(
            x=train_X,
            y=train_y,
            batch_size=32,
            epochs=80,
            validation_data=(dev_X, dev_y),
            shuffle=True,
            callbacks=[reduce_lr, earlystop, checkpoint]
            )
        model.load_weights(best_model_filepath)
        model.save('./checkpoint/dense_bilstm_crf_model.h5')

        pred = model.predict(test_X)

        from metrics import *
        y_true, y_pred = [], []

        for t_oh, p_oh in zip(test_y, pred):
            t_oh = np.argmax(t_oh, axis=1)
            t_oh = [id2tag[i].replace('_', '-') for i in t_oh if i != 0]
            p_oh = np.argmax(p_oh, axis=1)
            p_oh = [id2tag[i].replace('_', '-') for i in p_oh if i != 0]

            y_true.append(t_oh)
            y_pred.append(p_oh)

        f1 = f1_score(y_true, y_pred, suffix=False)
        p = precision_score(y_true, y_pred, suffix=False)
        r = recall_score(y_true, y_pred, suffix=False)
        acc = accuracy_score(y_true, y_pred)
    print("f1_score: {:.4f}, precision_score: {:.4f}, recall_score: {:.4f}, accuracy_score: {:.4f}".format(f1, p, r, acc))
    print(classification_report(y_true, y_pred, digits=4, suffix=False))