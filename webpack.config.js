//require our dependencies
var path = require('path')
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
//the base directory (abs. path) for resolving the entry option
    context: __dirname,
    entry: './assets/js/index',

    output: {
        //where to store compiled bundle
        path: path.resolve('./assets/bundles/'),
        //webpack naming convention where files are stores
        filename: '[name]-[hash].js',

    },

    plugins: [
        //where to store meta-data about the bundle
        new BundleTracker({filename: './webpack-stats.json'}

        ),

        //making jquery available in every module
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery' : 'jquery'

        })


    ],

    module: {
        rules: [
            //regexp to tell webpack to use the following loaders (loaders=translation to plain javascript from JSX etc.)
            {test: /\.jsx?$/,
                //babel should not transpile all files
                exclude: /node_modules/,
                //use the babel loader
                use: [
                { loader: 'babel-loader',
                  query: {
                    //what will be dealing with (react code)
                    presets: ['react'],
                    plugins: ['transform-class-properties']


                }

              }

        ]

    },
           {
                test: /\.css$/,

                use: ['style-loader','css-loader']
           },

    ]
    },

    resolve: {
        //where to look for modules

        extensions: ['.js', '.jsx', '.css'],

    }

}