const webpack = require('webpack');
const ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
    entry: __dirname + '/app/app.module.js',
    output: {
        path: __dirname + '/bin',
        filename: 'bundle.js'
    },
    module: {
        loaders: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                query: {
                    cacheDirectory: true,
                    presets: ['env']
                }
            }
        ],
        rules: [
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({fallback: "style-loader", use: "css-loader"})
            }, {
                test: /\.html/,
                use: 'html-loader'
            }
        ]
    },
    plugins: [
        new ExtractTextPlugin('bundle.css'),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
            jquery: 'jquery',
        })
    ],
    devtool: 'inline-source-map',
    devServer: {
        contentBase: './app'
    }
};
