const path = require('path')
const { VueLoaderPlugin } = require('vue-loader')
const BundleTracker = require('webpack-bundle-tracker')

module.exports = (env = {}) => {
    return {
        mode: env.prod ? 'production' : 'development',
        devtool: env.prod ? 'source-map' : 'eval-cheap-module-source-map',
        entry: path.resolve(__dirname, './src/main.ts'),
        output: {
            path: path.resolve(__dirname, './dist'),
        },
        module: {
            rules: [
                {
                    test: /\.vue$/,
                    loader: 'vue-loader'
                },
                {
                    test: /\.css$/,
                    loader: 'css-loader'
                },
                {
                    test: /\.scss$/,
                    loader: 'sass-loader'
                },
                {
                    test: /\.ts$/,
                    loader: 'ts-loader',
                    options: {
                        appendTsSuffixTo: [/\.vue$/],
                    }
                }
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
            new BundleTracker({
                filename: './webpack-stats.json',
                publicPath: 'http://0.0.0.0:8080/'
            }),
        ],
        devServer: {
            headers: {
                'Access-Control-Allow-Origin': '\*',
            },
            host: '0.0.0.0',
            port: '8080',
            hot: true,
            static: __dirname,
            client: {
                overlay: true,
                logging: 'info',
                progress: true,
            },
        }
    }
}