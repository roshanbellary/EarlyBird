import { AppRegistry } from 'react-native';
import App from './App';

AppRegistry.registerComponent('YourAppName', () => App);
AppRegistry.runApplication('YourAppName', {
  rootTag: document.getElementById('root')
});