import 'react-native-gesture-handler';
/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */

import React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {Header} from 'react-native-elements';
import {StyleSheet} from 'react-native';

import {createMaterialTopTabNavigator} from '@react-navigation/material-top-tabs';
import CurrentData from './src/screens/CurrentData';
import PastData from './src/screens/PastData';

import logo from './src/assets/midsun_logo.png';

const Tab = createMaterialTopTabNavigator();

export default class App extends React.Component {
  render() {
    return (
      <NavigationContainer>
        <Header
          centerComponent={{text: "STRATEGY", style: {color: "#000000", fontSize: 18}}}
          containerStyle={styles.headerColour}
          // backgroundImage={logo}
          // backgroundImageStyle={styles.imageStyle}
        />
        <Tab.Navigator initialRouteName="Current" backBehavior="history">
          <Tab.Screen name="Current" component={CurrentData}/>
          <Tab.Screen name="Past" component={PastData}/>
        </Tab.Navigator>
      </NavigationContainer>
    );
  }
  
};

const styles = StyleSheet.create({
  headerColour: {
    backgroundColor:'#FFFFFF',
  }
});