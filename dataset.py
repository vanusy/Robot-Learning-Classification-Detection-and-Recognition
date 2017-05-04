import glob
import numpy as nmpy

# Local dependencies
import constants

testPath = "test/*.png"

class Dataset:
    """
    This class manages the information for the dataset.
    """

    def __init__(self, path):
        """
        Initialize the Dataset object.

        Args:
            path: The path on where the dataset of images is stored.

        Returns:
            void
        """
        self.path = path
        self.train_set = []
        self.test_set = []
        self.classes = []
        self.classes_counts = []

    def generate_sets(self):
        """
        Reads the information of the training and testings sets and stores it into attributes of the object.

        Returns:
            void
        """
        dataset_classes = glob.glob(self.path + "/*")
	#print self.path
        for folder in dataset_classes:
            #print folder
	    path = folder.replace("\\", "/")
	    
            if "/" in folder:
                class_name = folder.split("/")[-1]
		#print class_name
            else:
                class_name = folder.split("\\")[-1]
            self.classes.append(class_name)
            train = glob.glob(path + "/*.png")
            test = glob.glob("test/*")
            self.train_set.append(train)
            self.test_set.append(test)
            self.classes_counts.append(0)
        #self.test_set = glob.glob("test/*")
	#print self.test_set

    def get_train_set(self):
        """
        Get the paths of the objects in the training set.

        Returns:
            list of strings: Paths for objects in the training set.
        """
        if len(self.train_set) == 0:
            self.generate_sets()
        return self.train_set

    def get_test_set(self):
        """
        Get the paths of the objects in the testing set.

        Returns:
            list of strings: Paths for objects in the testing set.
        """
        if len(self.test_set) == 0:
            self.generate_sets()
        return self.test_set

    def get_classes(self):
        """
        Get the names of the classes that are in the dataset.

        Returns:
            list of strings: List with the names of the classes.
        """
        if len(self.classes) == 0:
            self.generate_sets()
        return self.classes

    def get_classes_counts(self):
        """
        Get a list with the count of total local descriptors for each class.

        Returns:
            list of integers: List with the count of all the local descriptors in each class.
        """
        return self.classes_counts

    def get_y(self, my_set):
        """
        Get the labels for the a given set.

        Args:
            my_set (matrix of strings): Each row has the paths for the objects in that class.

        Returns:
            NumPy float array: The labels for a given set.
        """
        y = []
        if len(my_set) == 0:
            self.generate_sets()
        for class_ID in range(len(my_set)):
                y += [class_ID] * len(my_set[class_ID])
        # Transform the list in to a vector
        y = nmpy.float32(y)[:, nmpy.newaxis]
        return y

    def get_train_y(self):
        """
        Get the labels for the training set.

        Returns:
            NumPy float array: The labels for the training set.
        """
        return self.get_y(self.train_set)

    def get_test_y(self):
        """
        Get the labels for the testing set.

        Returns:
            NumPy float array: The labels for the testing set.
        """
        return self.get_y(self.test_set)

    def store_listfile(self):
        """
        Used for creating files in the format filelist used in Caffe for
        converting an image set. (caffe/tools/convert_imageset.cpp)

        Returns:
            void
        """
        train_file = open(constants.TRAIN_TXT_FILE, "w")
        test_file = open(constants.TEST_TXT_FILE, "w")
        self.get_train_set()
        self.get_test_set()
        for class_id in range(len(self.classes)):
            current_train = self.train_set[class_id]
            for filename in current_train:
                # Changing path in Windows
                path = filename.replace("\\", "/")
                idx = path.index("/")
                path = path[(idx + 1):]
                train_file.write("{0} {1}\n".format(path, class_id))
            current_test = self.test_set[class_id]
            for filename in current_test:
                # Changing path in Windows
                path = filename.replace("\\", "/")
                idx = path.index("/")
                path = path[(idx + 1):]
                test_file.write("{0} {1}\n".format(path, class_id))
        train_file.close()
        test_file.close()

    def set_class_count(self, class_number, class_count):
        """
        Set the count of local descriptors in one class.

        Args:
            class_number: ID for the class.
            class_count:  Number of local descriptors that were found in the class.

        Returns:
            void
        """
        self.classes_counts[class_number] = class_count
