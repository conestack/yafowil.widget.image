import {ImageWidget} from '../src/widget.js';
import $ from 'jquery';

QUnit.test('initialize', assert => {
    let el = $('<input />').addClass('image').appendTo('body');
    ImageWidget.initialize();
    let wid = el.data('yafowil-image');

    assert.ok(wid);
});