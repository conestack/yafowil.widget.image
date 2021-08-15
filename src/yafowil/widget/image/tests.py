from decimal import Decimal
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.compat import IS_PY2
from yafowil.tests import fxml
from yafowil.tests import YafowilTestCase
from yafowil.widget.image.utils import aspect_ratio_approximate
from yafowil.widget.image.utils import same_aspect_ratio
from yafowil.widget.image.utils import scale_size
import PIL
import pkg_resources
import unittest
import yafowil.loader  # noqa


if IS_PY2:
    from StringIO import StringIO
else:
    from importlib import reload
    from io import BytesIO as StringIO


class TestUtils(unittest.TestCase):

    def test_aspect_ratio_approximate(self):
        self.assertEqual(
            aspect_ratio_approximate((640, 480)),
            Decimal('1.33')
        )
        self.assertEqual(
            aspect_ratio_approximate((4, 3)),
            Decimal('1.33')
        )

    def test_same_aspect_ratio(self):
        self.assertTrue(same_aspect_ratio((640, 480), (4, 3)))
        self.assertFalse(same_aspect_ratio((1280, 1024), (4, 3)))

    def test_scale_size(self):
        self.assertEqual(scale_size((640, 480), (800, None)), (800, 600))
        self.assertEqual(scale_size((640, 480), (None, 3)), (4, 3))


class TestImageWidget(YafowilTestCase):

    def setUp(self):
        super(TestImageWidget, self).setUp()
        from yafowil.widget.image import widget
        reload(widget)

    def dummy_file_data(self, filename):
        path = pkg_resources.resource_filename(
            'yafowil.widget.image', 'testing/%s' % filename)
        with open(path, 'rb') as file:
            data = file.read()
        return data

    @property
    def dummy_png(self):
        return self.dummy_file_data('dummy.png')

    @property
    def dummy_jpg(self):
        return self.dummy_file_data('dummy.jpg')

    @property
    def dummy_pdf(self):
        return self.dummy_file_data('dummy.pdf')

    def test_dummy_file_data(self):
        dummy_png = self.dummy_png
        self.assertTrue(dummy_png.startswith(b'\x89PNG\r\n'))
        self.assertTrue(dummy_png.endswith(b'\x00IEND\xaeB`\x82'))

        dummy_jpg = self.dummy_jpg
        self.assertTrue(dummy_jpg.startswith(b'\xff\xd8\xff\xe0\x00\x10JFIF'))
        self.assertTrue(dummy_jpg.endswith(b'\xff\xd9'))

        dummy_pdf = self.dummy_pdf
        self.assertTrue(dummy_pdf.startswith(b'%PDF-1.5\n%'))
        self.assertTrue(dummy_pdf.endswith(b'\n956\n%%EOF\n'))

    def test_render_empty(self):
        form = factory(
            'form',
            name='myform',
            props={
                'action': 'myaction'
            })
        form['image'] = factory('image')
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <input accept="image/*" class="image" id="input-myform-image"
                 name="myform.image" type="file"/>
        </form>
        """, fxml(form()))

    def test_render_with_preset_value(self):
        # Image with value. Default file action keep is checked
        form = factory(
            'form',
            name='myform',
            props={
                'action': 'myaction'
            })
        form['image'] = factory(
            'image',
            value={
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            })
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <input accept="image/*" class="image" id="input-myform-image"
                 name="myform.image" type="file"/>
          <div id="radio-myform-image-keep">
            <input checked="checked" class="image" id="input-myform-image-keep"
                   name="myform.image-action" type="radio" value="keep"/>
            <span>Keep Existing image</span>
          </div>
          <div id="radio-myform-image-replace">
            <input class="image" id="input-myform-image-replace"
                   name="myform.image-action" type="radio" value="replace"/>
            <span>Replace existing image</span>
          </div>
          <div id="radio-myform-image-delete">
            <input class="image" id="input-myform-image-delete"
                   name="myform.image-action" type="radio" value="delete"/>
            <span>Delete existing image</span>
          </div>
        </form>
        """, fxml(form()))

    def test_render_with_preset_value_src_property(self):
        # If file URL of existing image is known, ``src`` property can be set
        # do display image above controls
        form = factory(
            'form',
            name='myform',
            props={
                'action': 'myaction'
            })
        form['image'] = factory(
            'image',
            value={
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            },
            props={
                'src': 'http://www.example.com/someimage.png',
                'alt': 'Alternative text'
            })
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <img alt="Alternative text" class="image-preview"
               id="image-preview-myform-image"
               src="http://www.example.com/someimage.png?nocache=..."/>
          <input accept="image/*" class="image" id="input-myform-image"
                 name="myform.image" type="file"/>
          ...
        </form>
        """, fxml(form()))

    def test_render_with_preset_value_src_property_get_params(self):
        # Src property may contain get parameters
        form = factory(
            'form',
            name='myform',
            props={
                'action': 'myaction'
            })
        form['image'] = factory(
            'image',
            value={
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            },
            props={
                'src': 'http://www.example.com/someimage?format=png',
                'alt': 'Alternative text'
            })
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <img alt="Alternative text" class="image-preview"
               id="image-preview-myform-image"
               src="http://www.example.com/someimage?format=png&amp;nocache=..."/>
          <input accept="image/*" class="image" id="input-myform-image"
                 name="myform.image" type="file"/>
          ...
        </form>
        """, fxml(form()))

    def test_render_with_preset_value_src_property_callable(self):
        # Src property can be callable
        form = factory(
            'form',
            name='myform',
            props={
                'action': 'myaction'
            })
        form['image'] = factory(
            'image',
            value={
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            },
            props={
                'src': lambda w, d: 'http://www.example.com/otherimage.png',
                'alt': 'Alternative text'
            })
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <img alt="Alternative text" class="image-preview"
               id="image-preview-myform-image"
               src="http://www.example.com/otherimage.png?nocache=..."/>
          <input accept="image/*" class="image" id="input-myform-image"
                 name="myform.image" type="file"/>
          ...
        </form>
        """, fxml(form()))

    def test_render_display(self):
        # Render in display mode
        form = factory(
            'form',
            name='myform',
            props={
                'action': 'myaction'
            })
        form['image'] = factory(
            'image',
            value={
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            },
            props={
                'src': 'http://www.example.com/someimage.png',
                'alt': 'Alternative text'
            },
            mode='display')
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <img alt="Alternative text"
               src="http://www.example.com/someimage.png"/>
        </form>
        """, fxml(form()))

        # Rendering is skipped if no source
        form['image'].attrs['src'] = None
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data"
              id="form-myform" method="post" novalidate="novalidate"/>
        """, fxml(form()))

    def test_extract_empty(self):
        # Extract empty (submitted but no upload)
        image = factory(
            'image',
            name='image')
        data = image.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, None)

    def test_extract_new(self):
        # Extract ``new``
        image = factory(
            'image',
            name='image')
        data = image.extract({
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        })
        self.assertEqual(data.errors, [])
        self.assertEqual(data.value, UNSET)
        self.check_output("""
        [('action', 'new'),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))

    def test_extract_keep(self):
        # Extract ``keep`` returns original value::
        image = factory(
            'image',
            name='image',
            value={
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            })
        data = image.extract({
            'image': {
                'file': StringIO(self.dummy_jpg),
                'mimetype': 'image/jpg'
            },
            'image-action': 'keep'
        })
        self.assertEqual(data.errors, [])
        self.check_output("""
        [('action', 'keep'),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.value.items())))
        self.check_output("""
        [('action', 'keep'),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))
        extracted = data.extracted['file'].read()
        self.assertTrue(extracted.startswith(b'\x89PNG\r\n'))
        self.assertTrue(extracted.endswith(b'\xaeB`\x82'))

    def test_extract_replace(self):
        # Extract ``replace`` returns new value
        image = factory(
            'image',
            name='image',
            value={
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            })
        data = image.extract({
            'image': {
                'file': StringIO(self.dummy_jpg),
                'mimetype': 'image/jpg'
            },
            'image-action': 'replace'
        })
        self.assertEqual(data.errors, [])
        self.check_output("""
        [('action', 'replace'),
        ('file', <... at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.value.items())))
        self.check_output("""
        [('action', 'replace'),
        ('file', <... at ...>),
        ('image', <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=50x50 at ...>),
        ('mimetype', 'image/jpg')]
        """, str(sorted(data.extracted.items())))
        extracted = data.extracted['file'].read()
        self.assertTrue(extracted.startswith(b'\xff\xd8\xff\xe0\x00\x10JFIF'))
        self.assertTrue(extracted.endswith(b'\xff\xd9'))

    def test_extract_delete(self):
        # Extract ``delete`` returns UNSET
        image = factory(
            'image',
            name='image',
            value={
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            })
        data = image.extract({
            'image': {
                'file': StringIO(self.dummy_jpg),
                'mimetype': 'image/jpg'
            },
            'image-action': 'delete'
        })
        self.assertEqual(data.errors, [])
        self.check_output("""
        [('action', 'delete'),
        ('file', <UNSET>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.value.items())))
        self.check_output("""
        [('action', 'delete'),
        ('file', <UNSET>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))

    def test_extract_mimetype_empty(self):
        # Image ``accept`` might be undefined.
        image = factory(
            'image',
            name='image',
            props={
                'accept': ''
            })
        data = image.extract({
            'image': {
                'file': StringIO(self.dummy_jpg),
                'mimetype': 'image/jpg'
            }
        })
        self.check_output("""
        [('action', 'new'),
        ('file', <... at ...>),
        ('image', <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=50x50 at ...),
        ('mimetype', 'image/jpg')]
        """, str(sorted(data.extracted.items())))

    def test_extract_mimetype_incompatible(self):
        # If set ``accept`` must be of type ``image/*``
        image = factory(
            'image',
            name='image',
            props={
                'accept': 'text/*'
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_jpg),
                'mimetype': 'image/jpg'
            }
        }
        err = self.expect_error(
            ValueError,
            image.extract,
            request
        )
        self.assertEqual(str(err), 'Incompatible mimetype text/*')

    def test_extract_mimetype_wrong_type(self):
        image = factory(
            'image',
            name='image',
            props={
                'accept': 'image/png'
            })
        data = image.extract({
            'image': {
                'file': StringIO(self.dummy_jpg),
                'mimetype': 'image/jpg'
            }
        })
        self.assertEqual(
            data.errors,
            [ExtractionError('Uploaded image not of type png')]
        )

    def test_extract_mimetype_success(self):
        image = factory(
            'image',
            name='image',
            props={
                'accept': 'image/jpg'
            })
        data = image.extract({
            'image': {
                'file': StringIO(self.dummy_jpg),
                'mimetype': 'image/jpg'
            }
        })
        self.check_output("""
        [('action', 'new'),
        ('file', <... at ...>),
        ('image', <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=50x50 at ...>),
        ('mimetype', 'image/jpg')]
        """, str(sorted(data.extracted.items())))

    def test_extract_mimtype_not_image(self):
        # Uploded file not an image
        image = factory(
            'image',
            name='image',
            props={
                'accept': 'image/*'
            })
        data = image.extract({
            'image': {
                'file': StringIO(self.dummy_pdf),
                'mimetype': 'application/pdf'
            }
        })
        self.assertEqual(
            data.errors,
            [ExtractionError('Uploaded file is not an image.')]
        )

    def test_extract_from_image_foundations(self):
        buffer = StringIO(self.dummy_png)
        image = PIL.Image.open(buffer)
        self.check_output("""
        <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>
        """, str(image))
        buffer.seek(0)
        data = buffer.read()
        self.assertTrue(data.startswith(b'\x89PNG\r\n'))
        self.assertTrue(data.endswith(b'\xaeB`\x82'))
        self.assertEqual(image.size, (50, 50))
        self.assertEqual(round(image.info['dpi'][0]), 72)
        self.assertEqual(round(image.info['dpi'][1]), 72)

    def test_extract_size_minsize(self):
        image = factory(
            'image',
            name='image',
            props={
                'minsize': (60, 60)
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.assertEqual(
            data.errors,
            [ExtractionError('Image must have a minimum size of 60 x 60 pixel')]
        )
        image = factory(
            'image',
            name='image',
            props={
                'minsize': (40, 40)
            })
        data = image.extract(request)
        self.assertEqual(data.errors, [])

    def test_extract_size_maxsize(self):
        image = factory(
            'image',
            name='image',
            props={
                'maxsize': (40, 40)
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.assertEqual(
            data.errors,
            [ExtractionError('Image must have a maximum size of 40 x 40 pixel')]
        )
        image = factory(
            'image',
            name='image',
            props={
                'maxsize': (60, 60)
            })
        data = image.extract(request)
        self.assertEqual(data.errors, [])

    def test_extract_size_exact(self):
        image = factory(
            'image',
            name='image',
            props={
                'minsize': (40, 40),
                'maxsize': (40, 40)
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.assertEqual(
            data.errors,
            [ExtractionError('Image must have a size of 40 x 40 pixel')]
        )
        image = factory(
            'image',
            name='image',
            props={
                'minsize': (50, 50),
                'maxsize': (50, 50)
            })
        data = image.extract(request)
        self.assertEqual(data.errors, [])

    def test_extract_dpi_min(self):
        # Minimum DPI
        image = factory(
            'image',
            name='image',
            props={
                'mindpi': (80, 80)
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.assertEqual(
            data.errors,
            [ExtractionError('Image must have at least 80 x 80 DPI')]
        )
        image = factory(
            'image',
            name='image',
            props={
                'mindpi': (60, 60)
            })
        data = image.extract(request)
        self.assertEqual(data.errors, [])

    def test_extract_dpi_max(self):
        # Maximum DPI
        image = factory(
            'image',
            name='image',
            props={
                'maxdpi': (60, 60)
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.assertEqual(
            data.errors,
            [ExtractionError('Image must have a maximum of 60 x 60 DPI')]
        )
        image = factory(
            'image',
            name='image',
            props={
                'maxdpi': (80, 80)
            })
        data = image.extract(request)
        self.assertEqual(data.errors, [])

    def test_extract_dpi_exact(self):
        # Exact DPI
        image = factory(
            'image',
            name='image',
            props={
                'mindpi': (60, 60),
                'maxdpi': (60, 60)
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.assertEqual(
            data.errors,
            [ExtractionError('Image must have a resolution of 60 x 60 DPI')]
        )
        image = factory(
            'image',
            name='image',
            props={
                'mindpi': (72, 72),
                'maxdpi': (72, 72)
            })
        data = image.extract(request)
        self.assertEqual(data.errors, [])

    def test_extract_scales(self):
        image = factory(
            'image',
            name='image',
            props={
                'scales': {
                    'micro': (20, 20),
                    'landscape': (70, 40),
                    'portrait': (40, 70)
                }
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.assertEqual(
            sorted(data.extracted.keys()),
            ['action', 'file', 'image', 'mimetype', 'scales']
        )
        self.assertEqual(data.extracted['action'], 'new')
        self.assertEqual(data.extracted['mimetype'], 'image/png')
        self.check_output("""
        <... at ...>
        """, str(data.extracted['file']))
        self.check_output("""
        <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>
        """, str(data.extracted['image']))
        self.check_output("""
        [('landscape', <PIL.Image.Image image mode=RGBA size=40x40 at ...>),
        ('micro', <PIL.Image.Image image mode=RGBA size=20x20 at ...>),
        ('portrait', <PIL.Image.Image image mode=RGBA size=40x40 at ...>)]
        """, str(sorted(data.extracted['scales'].items())))
        # save images to testing folder for manual inspection
        for name, image in data.extracted['scales'].items():
            path = pkg_resources.resource_filename(
                'yafowil.widget.image', 'testing/%s.png' % name)
            image.save(path, quality=100)

    def test_extract_from_image_cropping_foundations(self):
        buffer = StringIO(self.dummy_png)
        image = PIL.Image.open(buffer)
        buffer.seek(0)
        data = buffer.read()
        # save cropped image to testing folder for manual inspection
        left, top, width, height = 7, 3, 30, 40
        cropped = image.crop((left, top, width, height))
        path = pkg_resources.resource_filename(
            'yafowil.widget.image', 'testing/cropped.png')
        cropped.save(path, quality=100)
        # fitting logic
        self.assertTrue(same_aspect_ratio((300, 200), (600, 400)))
        # scale X down
        self.assertEqual(scale_size((100, 50), (75, None)), (75, 37))
        # scale X up
        self.assertEqual(scale_size((100, 50), (150, None)), (150, 75))
        # scale Y down
        self.assertEqual(scale_size((100, 50), (None, 25)), (50, 25))
        # scale Y up
        self.assertEqual(scale_size((100, 50), (None, 100)), (200, 100))
        # scale x
        size_from = (60, 40)
        self.assertEqual(aspect_ratio_approximate(size_from), Decimal('1.50'))
        size_to = (50, 25)
        self.assertEqual(aspect_ratio_approximate(size_to), Decimal('2.00'))
        self.assertTrue(
            aspect_ratio_approximate(size_from) <
            aspect_ratio_approximate(size_to)
        )
        scaled = scale_size(size_from, (size_to[0], None))
        self.assertEqual(scaled, (50, 33))
        offset_y = (scaled[1] - size_to[1]) / 2
        self.assertEqual(offset_y, 4)
        # scale y
        size_from = (60, 40)
        self.assertEqual(aspect_ratio_approximate(size_from), Decimal('1.50'))
        size_to = (50, 35)
        self.assertEqual(aspect_ratio_approximate(size_to), Decimal('1.43'))
        self.assertTrue(
            aspect_ratio_approximate(size_from) >
            aspect_ratio_approximate(size_to)
        )
        scaled = scale_size(size_from, (None, size_to[1]))
        self.assertEqual(scaled, (52, 35))
        offset_x = (scaled[0] - size_to[0]) / 2
        self.assertEqual(offset_x, 1)

    def test_extract_crop_as_is_without_offset_20_20(self):
        # Crop as is without offset, size (20, 20)
        image = factory(
            'image',
            name='image',
            props={
                'crop': {
                    'size': (20, 20)
                }
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.check_output("""
        [('action', 'new'),
        ('cropped', <PIL.Image.Image image mode=RGBA size=20x20 at ...>),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))
        # save cropped image to testing folder for manual inspection
        path = pkg_resources.resource_filename(
            'yafowil.widget.image', 'testing/crop_size_20_20.png')
        data.extracted['cropped'].save(path, quality=100)

    def test_extract_crop_as_is_without_offset_40_20(self):
        # Crop as is without offset, size (40, 20)
        image = factory(
            'image',
            name='image',
            props={
                'crop': {
                    'size': (40, 20)
                }
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.check_output("""
        [('action', 'new'),
        ('cropped', <PIL.Image.Image image mode=RGBA size=40x20 at ...>),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))
        # save cropped image to testing folder for manual inspection
        path = pkg_resources.resource_filename(
            'yafowil.widget.image', 'testing/crop_size_40_20.png')
        data.extracted['cropped'].save(path, quality=100)

        dummy_40_20_png = self.dummy_file_data('crop_size_40_20.png')
        self.assertTrue(dummy_40_20_png.startswith(b'\x89PNG\r\n'))
        self.assertTrue(dummy_40_20_png.endswith(b'\x00IEND\xaeB`\x82'))

    def test_extract_crop_as_is_without_offset_20_40(self):
        # Crop as is without offset, size (20, 40)
        image = factory(
            'image',
            name='image',
            props={
                'crop': {
                    'size': (20, 40)
                }
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.check_output("""
        [('action', 'new'),
        ('cropped', <PIL.Image.Image image mode=RGBA size=20x40 at ...>),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))
        # save cropped image to testing folder for manual inspection
        path = pkg_resources.resource_filename(
            'yafowil.widget.image', 'testing/crop_size_20_40.png')
        data.extracted['cropped'].save(path, quality=100)

        dummy_20_40_png = self.dummy_file_data('crop_size_20_40.png')
        self.assertTrue(dummy_20_40_png.startswith(b'\x89PNG\r\n'))
        self.assertTrue(dummy_20_40_png.endswith(b'\x00IEND\xaeB`\x82'))

    def test_extract_crop_with_offset_5_3_size_20_40(self):
        # Crop with offset (5, 3), size (20, 40)
        image = factory(
            'image',
            name='image',
            props={
                'crop': {
                    'size': (20, 40),
                    'offset': (5, 3)
                }
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.check_output("""
        [('action', 'new'),
        ('cropped', <PIL.Image.Image image mode=RGBA size=20x40 at ...>),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))
        # save cropped image to testing folder for manual inspection
        path = pkg_resources.resource_filename(
            'yafowil.widget.image', 'testing/crop_size_20_40_offset_5_3.png')
        data.extracted['cropped'].save(path, quality=100)

    def test_crop_with_offset_5_0_size_50_20(self):
        # Crop with offset (5, 0), size (50, 20) -> x overflow
        image = factory(
            'image',
            name='image',
            props={
                'crop': {
                    'size': (50, 20),
                    'offset': (5, 0)
                }
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.check_output("""
        [('action', 'new'),
        ('cropped', <PIL.Image.Image image mode=RGBA size=50x20 at ...>),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))
        # save cropped image to testing folder for manual inspection
        path = pkg_resources.resource_filename(
            'yafowil.widget.image', 'testing/crop_size_50_20_offset_5_0.png')
        data.extracted['cropped'].save(path, quality=100)

    def test_extract_crop_fitting_from_lanscape_30_18(self):
        # Crop fitting from lanscape, size (30, 18)
        # NOTE: this test case depends on
        #     ``test_extract_crop_as_is_without_offset_40_20`` to be executed,
        #     which is actually the case since dependency function name comes
        #     prior to ``test_extract_crop_fitting_from_lanscape_30_18`` in
        #     alpabetical order.
        image = factory(
            'image',
            name='image',
            props={
                'crop': {
                    'size': (30, 18),
                    'fitting': True
                }
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_file_data('crop_size_40_20.png')),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.check_output("""
        [('action', 'new'),
        ('cropped', <PIL.Image.Image image mode=RGBA size=30x18 at ...>),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=40x20 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))
        # save cropped image to testing folder for manual inspection
        path = pkg_resources.resource_filename(
            'yafowil.widget.image', 'testing/crop_fitting_ls_30_18.png')
        data.extracted['cropped'].save(path, quality=100)

    def test_extract_crop_fitting_from_landscape_18_30(self):
        # Crop fitting from landscape, size (18, 30)
        # NOTE: this test case depends on
        #     ``test_extract_crop_as_is_without_offset_40_20`` to be executed,
        #     which is actually the case since dependency function name comes
        #     prior to ``test_extract_crop_fitting_from_lanscape_18_30`` in
        #     alpabetical order.
        image = factory(
            'image',
            name='image',
            props={
                'crop': {
                    'size': (18, 30),
                    'fitting': True
                }
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_file_data('crop_size_40_20.png')),
                'mimetype': 'image/png'
            },
        }
        data = image.extract(request)
        self.check_output("""
        [('action', 'new'),
        ('cropped', <PIL.Image.Image image mode=RGBA size=18x30 at ...>),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=40x20 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))
        # save cropped image to testing folder for manual inspection
        path = pkg_resources.resource_filename(
            'yafowil.widget.image', 'testing/crop_fitting_ls_18_30.png')
        data.extracted['cropped'].save(path, quality=100)

    def test_extract_crop_fitting_from_portrait_30_18(self):
        # Crop fitting from portrait, size (30, 18)
        # NOTE: this test case depends on
        #     ``test_extract_crop_as_is_without_offset_20_40`` to be executed,
        #     which is actually the case since dependency function name comes
        #     prior to ``test_extract_crop_fitting_from_portrait_30_18`` in
        #     alpabetical order.
        image = factory(
            'image',
            name='image',
            props={
                'crop': {
                    'size': (30, 18),
                    'fitting': True
                }
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_file_data('crop_size_20_40.png')),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.check_output("""
        [('action', 'new'),
        ('cropped', <PIL.Image.Image image mode=RGBA size=30x18 at ...>),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=20x40 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))
        # save cropped image to testing folder for manual inspection
        path = pkg_resources.resource_filename(
            'yafowil.widget.image', 'testing/crop_fitting_pt_30_18.png')
        data.extracted['cropped'].save(path, quality=100)

    def test_extract_crop_fitting_from_portrait_18_30(self):
        # Crop fitting from portrait, size (18, 30)
        # NOTE: this test case depends on
        #     ``test_extract_crop_as_is_without_offset_20_40`` to be executed,
        #     which is actually the case since dependency function name comes
        #     prior to ``test_extract_crop_fitting_from_portrait_18_30`` in
        #     alpabetical order.
        image = factory(
            'image',
            name='image',
            props={
                'crop': {
                    'size': (18, 30),
                    'fitting': True
                }
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_file_data('crop_size_20_40.png')),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.check_output("""
        [('action', 'new'),
        ('cropped', <PIL.Image.Image image mode=RGBA size=18x30 at ...>),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=20x40 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))
        # save cropped image to testing folder for manual inspection
        path = pkg_resources.resource_filename(
            'yafowil.widget.image', 'testing/crop_fitting_pt_18_30.png')
        data.extracted['cropped'].save(path, quality=100)

    def test_extract_crop_fitting_square(self):
        # Crop fitting square -> thus also same ratio
        image = factory(
            'image',
            name='image',
            props={
                'crop': {
                    'size': (30, 30),
                    'fitting': True
                }
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.check_output("""
        [('action', 'new'),
        ('cropped', <PIL.Image.Image image mode=RGBA size=30x30 at ...>),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))
        # save cropped image to testing folder for manual inspection
        path = pkg_resources.resource_filename(
            'yafowil.widget.image', 'testing/crop_fitting_sq_30_30.png')
        data.extracted['cropped'].save(path, quality=100)

    def test_extract_crop_fitting_portrait_from_square(self):
        # Crop fitting portrait from square
        image = factory(
            'image',
            name='image',
            props={
                'crop': {
                    'size': (40, 50),
                    'fitting': True
                }
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.check_output("""
        [('action', 'new'),
        ('cropped', <PIL.Image.Image image mode=RGBA size=40x50 at ...>),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))
        # save cropped image to testing folder for manual inspection
        path = pkg_resources.resource_filename(
            'yafowil.widget.image', 'testing/crop_fitting_sq_40_50.png')
        data.extracted['cropped'].save(path, quality=100)

    def test_extract_crop_fitting_lanscape_from_square(self):
        # Crop fitting lanscape from square
        image = factory(
            'image',
            name='image',
            props={
                'crop': {
                    'size': (48, 40),
                    'fitting': True
                }
            })
        request = {
            'image': {
                'file': StringIO(self.dummy_png),
                'mimetype': 'image/png'
            }
        }
        data = image.extract(request)
        self.check_output("""
        [('action', 'new'),
        ('cropped', <PIL.Image.Image image mode=RGBA size=48x40 at ...>),
        ('file', <... at ...>),
        ('image', <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>),
        ('mimetype', 'image/png')]
        """, str(sorted(data.extracted.items())))
        # save cropped image to testing folder for manual inspection
        path = pkg_resources.resource_filename(
            'yafowil.widget.image', 'testing/crop_fitting_sq_48_40.png')
        data.extracted['cropped'].save(path, quality=100)

    def test_saving_image_data(self):
        # Save either by filename or file descriptor
        buffer = StringIO(self.dummy_png)
        image = PIL.Image.open(buffer)
        out = StringIO()
        image.save(out, 'png', quality=100)
        out.seek(0)
        data = out.read()
        self.assertTrue(data.startswith(b'\x89PNG\r\n'))
        self.assertTrue(data.endswith(b'\x00IEND\xaeB`\x82'))


if __name__ == '__main__':
    unittest.main()
