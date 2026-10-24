import $ from 'jquery';

export class ImageWidget {
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
        // the action radios are rendered next to the file input
        const name = `${this.elem.attr('name')}-action`;
        $(`input[name="${name}"][value="replace"]`, this.elem.parent()).trigger('click');
    }
}
