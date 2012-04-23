/*
 * yafowil image widget
 */

if (typeof(window['yafowil']) == "undefined") yafowil = {};

(function($) {

    $(document).ready(function() {
        // initial binding
        yafowil.image.binder();
        
        // add after ajax binding if bdajax present
        if (typeof(window['bdajax']) != "undefined") {
            $.extend(bdajax.binders, {
                imagewidget_binder: yafowil.image.binder
            });
        }
    });
    
    $.extend(yafowil, {
        
        image: {
            
            // XXX: same needed for file, provide in yafowil directly?
            binder: function(context) {
                $('input.image').bind('change', function(evt) {
                    var elem = $(this);
                    if (!elem.attr('type') == 'radio') {
                        return;
                    }
                    $('input.image[value="replace"]').trigger('click');
                });
            }
        }
    });

})(jQuery);