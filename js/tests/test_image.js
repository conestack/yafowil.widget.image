import $ from 'jquery';
import { ImageWidget } from '../src/default/widget.js';

QUnit.module('ImageWidget', (hooks) => {
    let container;

    function create_inputs(css) {
        const file = $(`<input type="file" class="${css}" />`).appendTo(container);
        const radios = {};
        for (const value of ['keep', 'replace', 'delete']) {
            radios[value] = $(`<input type="radio" name="${css}-action" class="${css}" />`)
                .attr('value', value)
                .appendTo(container);
        }
        radios.keep.prop('checked', true);
        return { file, radios };
    }

    hooks.beforeEach(() => {
        container = $('<div />').appendTo('body');
    });
    hooks.afterEach(() => {
        container.remove();
    });

    QUnit.test('initialize', (assert) => {
        const el = $('<input />').addClass('image').appendTo(container);
        ImageWidget.initialize();
        const wid = el.data('yafowil-image');
        assert.true(wid instanceof ImageWidget);
        assert.true(wid.elem.is(el));
    });

    QUnit.test('image file change selects replace action', (assert) => {
        const { file, radios } = create_inputs('image');
        new ImageWidget(file);
        file.trigger('change');
        assert.true(radios.replace.prop('checked'));
        assert.false(radios.keep.prop('checked'));
    });

    QUnit.test('image radio change is ignored', (assert) => {
        const { file, radios } = create_inputs('image');
        new ImageWidget(file);
        radios.delete.prop('checked', true).trigger('change');
        assert.true(radios.delete.prop('checked'));
        assert.false(radios.replace.prop('checked'));
    });

    QUnit.test('file change selects replace action', (assert) => {
        const { file, radios } = create_inputs('file');
        new ImageWidget(file);
        file.trigger('change');
        assert.true(radios.replace.prop('checked'));
        assert.false(radios.keep.prop('checked'));
    });

    QUnit.test('file radio change is ignored', (assert) => {
        const { file, radios } = create_inputs('file');
        new ImageWidget(file);
        radios.delete.prop('checked', true).trigger('change');
        assert.true(radios.delete.prop('checked'));
        assert.false(radios.replace.prop('checked'));
    });
});
