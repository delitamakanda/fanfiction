const path = require('path')
const { VueLoaderPlugin } = require('vue-loader')
const BundleTracker = require('webpack-bundle-tracker')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const webpack = require('webpack');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = (env = {}) => {
    return {
        mode: env.prod ? 'production' : 'development',
        devtool: env.prod ? 'source-map' : 'inline-source-map',
        entry: path.resolve(__dirname, './src/main.ts'),
        output: {
            path: path.resolve(__dirname, './dist'),
            chunkFilename: '[name].bundle.js'
        },
        optimization: {
            minimize: env.prod ? true : false
        },
        module: {
            rules: [
                {
                    test: /\.vue$/,
                    exclude: /node_modules/,
                    loader: 'vue-loader',
                },
                {
                    test: /\.css$/,
                    use: [
                        'style-loader',
                        {
                            loader: MiniCssExtractPlugin.loader,
                            options: {
                                esModule: false
                            }
                        },
                        {
                            loader: 'css-loader',
                            options: {
                                importLoaders: 1
                            }
                        },
                        'postcss-loader'
                    ]
                },
                {
                    test: /\.(js|jsx)$/,
                    exclude: /node_modules/,
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
                    },
                },
                {
                    test: /\.(ts|tsx)$/,
                    loader: 'ts-loader',
                    exclude: /node_modules/,
                    options: {
                        appendTsSuffixTo: [/\.vue$/],
                    }
                },
                {
                    test: /\.(woff|woff2|eot|ttf|svg|jpg|png)$/,
                    use: {
                        loader: 'file-loader',
                        options: {
                            name: '[path][name].[ext]',
                        },
                    },
                },
            ]
        },
        resolve: {
            extensions: ['.js', '.ts', '.vue', '.json'],
            alias: {
                'vue': '@vue/runtime-dom'
            }
        },
        plugins: [
            new VueLoaderPlugin(),
            new HtmlWebpackPlugin({
                template: path.resolve(__dirname, 'public/index.html')
            }),
            new BundleTracker({
                filename: './webpack-stats.json',
                publicPath: 'http://0.0.0.0:8080/'
            }),
            new MiniCssExtractPlugin({
                filename: '[name].css',
                chunkFilename: '[id].css',
            }),
            new webpack.ProvidePlugin({
                process: 'process/browser',
            }),
        ],
        devServer: {
            headers: {
                'Access-Control-Allow-Origin': '\*',
            },
            host: '0.0.0.0',
            port: '8080',
            hot: true,
            open: false,
            devMiddleware: {
                writeToDisk: false
            },
            static: {
                watch: true
            },
            client: {
                overlay: true,
                logging: 'info',
                progress: true,
            },
        },
        optimization: {
            minimizer: [
                new CssMinimizerPlugin(),
            ]
        }
    }
}