(function (exports, $) {
    'use strict';

    class ImageWidget {
        static initialize(context) {
            $('input.image', context).each(function (event) {
                new ImageWidget($(this));
            });
        }
        constructor(elem) {
            this.elem = elem;
            $('input.file').bind('change', function (evt) {
                let elem = $(this);
                if (elem.attr('type') === 'radio') {
                    return true;
                }
                $('input.file[value="replace"]').trigger('click');
            });
            $('input.image').bind('change', function (evt) {
                let elem = $(this);
                if (elem.attr('type') === 'radio') {
                    return true;
                }
                $('input.image[value="replace"]').trigger('click');
            });
        }
    }

    $(function() {
        if (window.ts !== undefined) {
            ts.ajax.register(ImageWidget.initialize, true);
        } else {
            ImageWidget.initialize();
        }
    });

    exports.ImageWidget = ImageWidget;

    Object.defineProperty(exports, '__esModule', { value: true });


    if (window.yafowil === undefined) {
        window.yafowil = {};
    }
    window.yafowil.image = exports;


    return exports;

})({}, jQuery);
//# sourceMappingURL=widget.js.map
