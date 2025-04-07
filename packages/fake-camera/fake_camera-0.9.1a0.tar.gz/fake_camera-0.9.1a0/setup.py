from distutils.core import setup

long_description = """Code Example:

>>> import time
>>> import cv2 as cv
>>> from fake_camera import Fake_Camera  # import the class
>>> fake_cam_object = FakeCamera().add_foreground_image().add_background_image().build() # create an instance of the fake camera class
>>> while True:
       snapshot = fake_cam_object.get_snapshot()  # get the next fake snapshot from from the fake camera
       cv.imshow("Moving Image", snapshot)
       time.sleep(1/10)
       if cv.waitKey(1) & 0xFF == ord("q"):
           break
"""

setup(
  name = 'fake-camera',
  packages = ['fake_camera'],
  version = 'v0.9.1-alpha',
  license='MIT',
  description = 'A Camera Simulator. It creates a moving image in the screen.',
  long_description = long_description,
  author = 'fjolublar',
  url = 'https://github.com/fjolublar/fake_camera',
  download_url = 'https://github.com/fjolublar/fake_camera/archive/v0.9.1-alpha.tar.gz',
  keywords = ['Fake Camera', 'Moving Image', 'Camera Simulator'],
  install_requires=['Pillow', 'numpy'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
  ],
)
