import $ from 'jquery';

export class ImageWidget {

    static initialize(context) {
        $('input.image', context).each(function (event) {
            new ImageWidget($(this));
        });
    }

    constructor(elem) {
        this.elem = elem;
        // XXX: file needs anyway, provide in yafowil directly?
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
