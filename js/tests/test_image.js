import $ from 'jquery';
import { ImageWidget } from '../src/default/widget.js';

QUnit.module('ImageWidget', (hooks) => {
    let container;

    // markup as rendered by the ``image`` blueprint with an existing value
    function create_widget(parent, name, radio_css = 'image') {
        const file = $('<input type="file" class="image" />').attr('name', name).appendTo(parent);
        const radios = {};
        for (const value of ['keep', 'replace', 'delete']) {
            radios[value] = $('<input type="radio" />')
                .addClass(radio_css)
                .attr('name', `${name}-action`)
                .attr('value', value);
            $('<div />').append(radios[value]).appendTo(parent);
        }
        radios.keep.prop('checked', true);
        return { file, radios };
    }

    function count_clicks(elem) {
        const counter = { clicks: 0 };
        elem.on('click', () => {
            counter.clicks++;
        });
        return counter;
    }

    hooks.beforeEach(() => {
        container = $('<div />').appendTo('body');
    });
    hooks.afterEach(() => {
        container.remove();
    });

    QUnit.test('initialize', (assert) => {
        const { file, radios } = create_widget(container, 'myform.image');
        ImageWidget.initialize();
        const wid = file.data('yafowil-image');
        assert.true(wid instanceof ImageWidget);
        assert.true(wid.elem.is(file));
        for (const radio of Object.values(radios)) {
            assert.strictEqual(radio.data('yafowil-image'), undefined);
        }
    });

    QUnit.test('file change selects replace action', (assert) => {
        const { file, radios } = create_widget(container, 'myform.image');
        ImageWidget.initialize();
        const counter = count_clicks(radios.replace);
        file.trigger('change');
        assert.strictEqual(counter.clicks, 1);
        assert.true(radios.replace.prop('checked'));
        assert.false(radios.keep.prop('checked'));
    });

    QUnit.test('file change with custom radio class', (assert) => {
        const { file, radios } = create_widget(container, 'myform.image', 'my_radio_input');
        ImageWidget.initialize();
        file.trigger('change');
        assert.true(radios.replace.prop('checked'));
        assert.false(radios.keep.prop('checked'));
    });

    QUnit.test('radio change is ignored', (assert) => {
        const { radios } = create_widget(container, 'myform.image');
        ImageWidget.initialize();
        radios.delete.prop('checked', true).trigger('change');
        assert.true(radios.delete.prop('checked'));
        assert.false(radios.replace.prop('checked'));
    });

    QUnit.test('file change only affects own widget', (assert) => {
        const form = $('<form />').appendTo(container);
        const first = create_widget(form, 'myform.first');
        const second = create_widget(form, 'myform.second');
        const other_form = $('<form />').appendTo(container);
        const other = create_widget(other_form, 'myform.first');
        ImageWidget.initialize();
        first.file.trigger('change');
        assert.true(first.radios.replace.prop('checked'));
        assert.true(second.radios.keep.prop('checked'));
        assert.true(other.radios.keep.prop('checked'));
    });

    QUnit.test('initialize context does not bind other widgets again', (assert) => {
        const first = create_widget(container, 'myform.first');
        ImageWidget.initialize();
        const context = $('<div />').appendTo(container);
        const second = create_widget(context, 'myform.second');
        ImageWidget.initialize(context);
        const first_counter = count_clicks(first.radios.replace);
        const second_counter = count_clicks(second.radios.replace);
        first.file.trigger('change');
        assert.strictEqual(first_counter.clicks, 1);
        assert.strictEqual(second_counter.clicks, 0);
        second.file.trigger('change');
        assert.strictEqual(first_counter.clicks, 1);
        assert.strictEqual(second_counter.clicks, 1);
    });
});
