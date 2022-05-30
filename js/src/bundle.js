import $ from 'jquery';

import {ImageWidget} from './widget.js';

export * from './widget.js';

$(function() {
    if (window.ts !== undefined) {
        ts.ajax.register(ImageWidget.initialize, true);
    } else if (window.bdajax !== undefined) {
        bdajax.register(ImageWidget.initialize, true);
    } else {
        ImageWidget.initialize();
    }
});
