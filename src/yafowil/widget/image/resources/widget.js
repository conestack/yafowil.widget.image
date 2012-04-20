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
            
            binder: function(context) {
            }
        }
    });

})(jQuery);