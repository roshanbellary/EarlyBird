module.exports = {
    // ... other webpack configurations
    resolve: {
      alias: {
        'react-native$': 'react-native-web'
      },
      extensions: ['.web.js', '.js']
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-react', '@babel/preset-env'],
              plugins: [
                '@babel/plugin-proposal-class-properties',
                '@babel/plugin-proposal-object-rest-spread'
              ]
            }
          }
        }
      ]
    }
  }