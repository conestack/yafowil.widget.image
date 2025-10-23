import cleanup from 'rollup-plugin-cleanup';
import postcss from 'rollup-plugin-postcss';
import terser from '@rollup/plugin-terser';

const out_dir = 'src/yafowil/widget/image/resources';

const outro = `
window.yafowil = window.yafowil || {};
window.yafowil.image = exports;
`;

export default args => {
    let conf = [];

    let bundle_default = {
        input: 'js/src/default/bundle.js',
        plugins: [
            cleanup()
        ],
        output: [{
            name: 'yafowil_image',
            file: `${out_dir}/default/widget.js`,
            format: 'iife',
            outro: outro,
            globals: {
                jquery: 'jQuery'
            },
            interop: 'default'
        }],
        external: [
            'jquery'
        ]
    };
    if (args.configDebug !== true) {
        bundle_default.output.push({
            name: 'yafowil_image',
            file: `${out_dir}/default/widget.min.js`,
            format: 'iife',
            plugins: [
                terser()
            ],
            outro: outro,
            globals: {
                jquery: 'jQuery'
            },
            interop: 'default'
        });
    }
    let scss_default = {
        input: ['scss/default/widget.scss'],
        output: [{
            file: `${out_dir}/default/widget.min.css`,
            format: 'es',
            plugins: [terser()],
        }],
        plugins: [
            postcss({
                extract: true,
                minimize: true,
                use: [
                    ['sass', { outputStyle: 'compressed' }],
                ],
            }),
        ],
    };
    conf.push(bundle_default, scss_default);

    return conf;
};
