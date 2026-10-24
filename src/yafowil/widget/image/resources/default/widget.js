var yafowil_image = (function (exports, $) {
    'use strict';

    class ImageWidget {
        static initialize(context) {
            $('input.image[type="file"]', context).each(function () {
                new ImageWidget($(this));
            });
        }
        constructor(elem) {
            elem.data('yafowil-image', this);
            this.elem = elem;
            this.on_change = this.on_change.bind(this);
            elem.on('change', this.on_change);
        }
        on_change() {
            const name = `${this.elem.attr('name')}-action`;
            $(`input[name="${name}"][value="replace"]`, this.elem.parent()).trigger('click');
        }
    }

    $(() => {
        if (window.ts !== undefined) {
            ts.ajax.register(ImageWidget.initialize, true);
        } else if (window.bdajax !== undefined) {
            bdajax.register(ImageWidget.initialize, true);
        } else {
            ImageWidget.initialize();
        }
    });

    exports.ImageWidget = ImageWidget;

    Object.defineProperty(exports, '__esModule', { value: true });


    window.yafowil = window.yafowil || {};
    window.yafowil.image = exports;


    return exports;

})({}, jQuery);
