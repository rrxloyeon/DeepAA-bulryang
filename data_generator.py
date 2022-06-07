import os
import copy
import logging
import numpy as np
import math
from PIL import Image
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
tf.get_logger().setLevel(logging.ERROR)
from tensorflow.keras.utils import Sequence
from augmentation import IMAGENET_SIZE, centerCrop_imagenet
import pdb


CIFAR_MEANS = np.array([0.49139968, 0.48215841, 0.44653091], dtype=np.float32)
CIFAR_STDS = np.array([0.2023, 0.1994, 0.2010], dtype=np.float32)

IMAGENET_MEANS = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STDS = np.array([0.229, 0.224, 0.225], dtype=np.float32)

def split_train_validation(x, y, val_size):
    indices = np.arange(len(x))
    np.random.shuffle(indices)
    x_train, x_val, y_train, y_val = x[:-val_size], x[-val_size:], y[:-val_size], y[-val_size:]
    return x_train,  y_train, x_val, y_val

def get_cifar100_data(num_classes=100, val_size=10000):
    (x_train_val, y_train_val), (x_test, y_test) = tf.keras.datasets.cifar100.load_data()
    y_train_val = y_train_val.squeeze()
    y_test = y_test.squeeze()
    if val_size > 0:
        x_train, y_train, x_val, y_val = split_train_validation(x_train_val, y_train_val, val_size=val_size)
    else:
        x_train, y_train = x_train_val, y_train_val
        x_val, y_val = None, None
    return x_train, y_train, x_val, y_val, x_test, y_test

def get_cifar10_data(num_classes=10, val_size=10000):
    (x_train_val, y_train_val), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    y_train_val = y_train_val.squeeze()
    y_test = y_test.squeeze()
    if val_size > 0:
        x_train, y_train, x_val, y_val = split_train_validation(x_train_val, y_train_val, val_size=val_size)
    else:
        x_train, y_train = x_train_val, y_train_val
        x_val, y_val = None, None

    return x_train, y_train, x_val, y_val, x_test, y_test

def get_nepes_data(data_root):
    classes_list = os.listdir(data_root)
    classes = {name: i for i, name in enumerate(classes_list)}
    num_classes = len(classes)

    x_train, y_train, x_val, y_val, x_test, y_test = [], [], [], [], [], []
    for key, value in classes.items(): #클래스 하나씩 접근
        file_list = os.listdir(os.path.join(data_root, key)) #해당 class의 파일 모두 file_list에 저장
        np.random.seed(0)
        np.random.shuffle(file_list)
        length = len(file_list) #해당 class의 사진 개수

        #어떤 클래스는 너무 작아서 충분한 데이터셋 확보 못해서 에러뜸.여기 어딘가 수정필요할듯
        for f in file_list[:int(0.6*length)]:
            with Image.open(os.path.join(data_root, key, f)) as img:
                x_train.append(np.array(img))
                y_train.append(np.uint8(value))
        print("{}:{}:len(x_train)={}".format(value, key, len(x_train)))

        for f in file_list[int(0.6*length):int(0.8*length)]:
            with Image.open(os.path.join(data_root, key, f)) as img:
                x_val.append(np.array(img))
                y_val.append(np.uint8(value))
        print("{}:{}:len(x_val)={}".format(value, key, len(x_val)))

        for f in file_list[int(0.8*length):]:
            with Image.open(os.path.join(data_root, key, f)) as img:
                x_test.append(np.array(img))
                y_test.append(np.uint8(value))
        print("{}:{}:len(x_test)={}".format(value, key, len(x_test)))

    x_train_arr = np.empty((len(x_train),400,400,3), dtype='uint8')
    x_val_arr = np.empty((len(x_val),400,400,3), dtype='uint8')
    x_test_arr = np.empty((len(x_test),400,400,3), dtype='uint8')

    for i in range(len(x_train)):
        if x_train[i].shape==(400,400,3):
            x_train_arr[i] = x_train[i]
    y_train = np.array(y_train)

    for i in range(len(x_val)):
        if x_val[i].shape==(400,400,3):
            x_val_arr[i] = x_val[i]
    y_val = np.array(y_val)

    for i in range(len(x_test)):
        if x_test[i].shape==(400,400,3):
            x_test_arr[i] = x_test[i]
    y_test = np.array(y_test)

    return x_train_arr, y_train, x_val_arr, y_val, x_test_arr, y_test, num_classes

def get_dmd_data(data_root):
    classes_list = os.listdir(data_root)
    classes = {name: i for i, name in enumerate(classes_list)}
    num_classes = len(classes)

    x_train, y_train, x_val, y_val, x_test, y_test = [], [], [], [], [], []
    for key, value in classes.items(): #클래스 하나씩 접근
        file_list = os.listdir(os.path.join(data_root, key)) #해당 class의 파일 모두 file_list에 저장
        np.random.seed(0)
        np.random.shuffle(file_list)
        length = len(file_list) #해당 class의 사진 개수

        #어떤 클래스는 너무 작아서 충분한 데이터셋 확보 못해서 에러뜸.여기 어딘가 수정필요할듯
        for f in file_list[:int(0.6*length)]:
            with Image.open(os.path.join(data_root, key, f)) as img:
                x_train.append(np.array(img))
                y_train.append(np.uint8(value))
        print("{}:{}:len(x_train)={}".format(value, key, len(x_train)))
        for f in file_list[int(0.6*length):int(0.8*length)]:
            with Image.open(os.path.join(data_root, key, f)) as img:
                x_val.append(np.array(img))
                y_val.append(np.uint8(value))
        print("{}:{}:len(x_val)={}".format(value, key, len(x_val)))
        for f in file_list[int(0.8*length):]:
            with Image.open(os.path.join(data_root, key, f)) as img:
                x_test.append(np.array(img))
                y_test.append(np.uint8(value))
        print("{}:{}:len(x_test)={}".format(value, key, len(x_test)))
        # pdb.set_trace() # shape of img (720, 1280, 3)
    
    x_train_arr = np.empty((len(x_train),720, 1280, 3), dtype='uint8')
    x_val_arr = np.empty((len(x_val),720, 1280, 3), dtype='uint8')
    x_test_arr = np.empty((len(x_test),720, 1280, 3), dtype='uint8')

    for i in range(len(x_train)):
        if x_train[i].shape==(720, 1280, 3):
            x_train_arr[i] = x_train[i]
    y_train = np.array(y_train)

    for i in range(len(x_val)):
        if x_val[i].shape==(720, 1280, 3):
            x_val_arr[i] = x_val[i]
    y_val = np.array(y_val)

    for i in range(len(x_test)):
        if x_test[i].shape==(720, 1280, 3):
            x_test_arr[i] = x_test[i]
    y_test = np.array(y_test)
    # pdb.set_trace() # check length of x_train_arr
    return x_train_arr, y_train, x_val_arr, y_val, x_test_arr, y_test, num_classes

class DataGenerator(Sequence):
    def __init__(self, 
                 data, 
                 labels,
                 img_dim=None,
                 batch_size=32, 
                 num_classes=10, 
                 shuffle=True,
                 drop_last=True,
                ):
        
        self._data = data
        self.data = self._data # initially without calling augment, the output data is not augmented
        self.labels = labels
        self.img_dim = img_dim
        self.batch_size = batch_size
        self.num_classes = num_classes
        self.shuffle = shuffle
        self.drop_last = drop_last
        self.on_epoch_end()

    def reset_augment(self):
        self.data = self._data

    def on_epoch_end(self):
        self.indices = np.arange(len(self._data))
        if self.shuffle:
            np.random.shuffle(self.indices)

    def sample_labeled_data_batch(self, label, bs): # bs = 16; DeepAA_search.py L#585 argumnet "val_bs=16"
        # suffle indices every time
        indices = np.arange(len(self._data))
        np.random.shuffle(indices)
        if isinstance(self.labels, list):
            labels = [self.labels[k] for k in indices]
        else: # val_ds : type(self.labels)=ndarray
            labels = self.labels[indices]
        matched_labels = np.array(labels) == int(label)
        matched_indices = [id for id, isMatched in enumerate(matched_labels) if isMatched]
        if len(matched_indices) - bs >=0:
            start_idx = np.random.randint(0, len(matched_indices)-bs)
            batch_indices = matched_indices[start_idx:start_idx + bs]
        else:
            print('Not enough matched data, required {}, but got {} instead'.format(bs, len(matched_indices)))
            batch_indices = matched_indices
        data_indices = indices[batch_indices]
        return [self.data[k] for k in data_indices], np.array([self.labels[k] for k in data_indices], dtype=self.labels[0].dtype)

    def __len__(self):
        if self.drop_last:
            return int(np.floor(len(self.data) / self.batch_size)) # drop the last batch
        else:
            return int(np.ceil(len(self.data) / self.batch_size)) # drop the last batch

    def __getitem__(self, idx):
        curr_batch = self.indices[idx*self.batch_size:(idx+1)*self.batch_size]
        batch_len = len(curr_batch)
        if isinstance(self.data, list) and isinstance(self.labels, list):
            return [self.data[k] for k in curr_batch], np.array([self.labels[k] for k in curr_batch], np.int32)
        else:
            return self.data[curr_batch], self.labels[curr_batch]

class DataAugmentation(object):
    def __init__(self, num_classes, dataset, image_shape, ops_list=None, default_pre_aug=None, default_post_aug=None):
        self.ops, self.op_names = ops_list
        self.default_pre_aug = default_pre_aug
        self.default_post_aug = default_post_aug
        self.num_classes = num_classes
        self.dataset = dataset
        self.image_shape = image_shape
        if 'imagenet' in self.dataset:
            assert self.image_shape == (*IMAGENET_SIZE, 3)
        elif 'cifar' in self.dataset:
            assert self.image_shape == (32, 32, 3)
        elif 'nepes' in self.dataset:
            assert self.image_shape == (*IMAGENET_SIZE, 3)
        elif 'dmd' in self.dataset:
            assert self.image_shape == (*IMAGENET_SIZE, 3)
        else:
            raise Exception('Unrecognized dataset')

    def sequantially_augment(self, args):
        idx, img_, op_idxs, mags, aug_finish = args
        assert img_.dtype == np.uint8, 'Input images should be unporocessed, should stay in np.uint8'
        img = copy.deepcopy(img_)
        pil_img = Image.fromarray(img)  # Convert to PIL.Image
        if self.default_pre_aug is not None:
            for op in self.default_pre_aug:
                pil_img = op(pil_img)
        if self.ops is not None:
            for op_idx, mag in zip(op_idxs, mags):
                op, minval, maxval = self.ops[op_idx]
                assert mag > -1e-5 and mag < 1. + 1e-5, 'magnitudes should be in the range of (0., 1.)'
                mag = mag * (maxval - minval) + minval
                pil_img = op(pil_img, mag)
        if self.default_post_aug is not None and self.use_post_aug:
            for op in self.default_post_aug:
                pil_img = op(pil_img, None)
        if 'cifar' in self.dataset:
            img = np.asarray(pil_img, dtype=np.uint8)
            return idx, img
        elif 'imagenet' in self.dataset:
            if aug_finish:
                pil_img = self.crop_IMAGENET(pil_img)
            img = np.asarray(pil_img, dtype=np.uint8)
            return idx, img
        elif 'nepes' in self.dataset:
            if aug_finish:
                pil_img = self.crop_IMAGENET(pil_img)
            img = np.asarray(pil_img, dtype=np.uint8)
            return idx, img
        elif 'dmd' in self.dataset:
            if aug_finish:
                pil_img = self.crop_IMAGENET(pil_img)
            img = np.asarray(pil_img, dtype=np.uint8)
            return idx, img
        else:
            raise Exception

    def postprocessing_standardization(self, pil_img):
        x = np.asarray(pil_img, dtype=np.float32) / 255.
        if 'cifar' in self.dataset:
            x = (x - CIFAR_MEANS) / CIFAR_STDS
        elif 'imagenet' in self.dataset:
            x = (x - IMAGENET_MEANS) / IMAGENET_STDS
        elif 'nepes' in self.dataset:
            x = (x - IMAGENET_MEANS) / IMAGENET_STDS
        elif 'dmd' in self.dataset:
            x = (x - IMAGENET_MEANS) / IMAGENET_STDS #
        else:
            raise Exception('Unrecoginized dataset')
        return x

    def crop_IMAGENET(self, img):
        # cropping imagenet dataset to the same size
        if isinstance(img, np.ndarray):
            assert img.shape == (IMAGENET_SIZE[1], IMAGENET_SIZE[0], 3) and img.dtype==np.uint8, 'numpy array should be {}, but got {}. crop_IMAGENET does not apply to numpy array, but got {}'.format(IMAGENET_SIZE, img.size, img.dtype)
            return img
        w, h = img.size
        if w == IMAGENET_SIZE[0] and h == IMAGENET_SIZE[1]:
            return img
        return centerCrop_imagenet(img, None)

    def check_data_type(self, images, labels):
        assert images[0].dtype == np.uint8
        if 'imagenet' in self.dataset:
            assert type(labels[0]) == np.int32
        elif 'cifar' in self.dataset:
            assert type(labels[0]) == np.uint8
        if 'nepes' in self.dataset:
            assert type(labels[0]) == np.uint8
        elif 'dmd' in self.dataset:
            assert type(labels[0]) == np.uint8
        else:
            raise Exception('Unrecognized dataset')

    def __call__(self, images, labels, samples_op, samples_mag, use_post_aug, pool=None, chunksize=None, aug_finish=True):
        self.check_data_type(images, labels)

        self.use_post_aug = use_post_aug
        self.batch_len = len(labels)
        if aug_finish:
            aug_imgs = np.empty([self.batch_len, *self.image_shape], dtype=np.float32)
        else:
            aug_imgs = [None]*self.batch_len
        aug_results = pool.imap_unordered(self.sequantially_augment,
                                          zip(range(self.batch_len), images, samples_op, samples_mag, [aug_finish]*self.batch_len),
                                          chunksize=math.ceil(float(self.batch_len) / float(pool._processes)) if chunksize is None else chunksize)
        for idx, img in aug_results:
            aug_imgs[idx] = img

        if aug_finish:
            aug_imgs = self.postprocessing_standardization(aug_imgs)

        return aug_imgs, labels