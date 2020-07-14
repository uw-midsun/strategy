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
import {StyleSheet, View, Image} from 'react-native';

import {createMaterialTopTabNavigator} from '@react-navigation/material-top-tabs';
import CurrentData from './src/screens/CurrentData';
import PastData from './src/screens/PastData';

import logo from './src/assets/midsun_logo.png';
import * as Constants from './src/constants';

const Tab = createMaterialTopTabNavigator();

export default class App extends React.Component {
  render() {
    return (
      <NavigationContainer>
        <View style={styles.carDisplay}>
          <Image style = {styles.imageStyling} source={logo}/>
        </View>
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
  },
  imageStyling: {
    width: Constants.widthOfBoxes * 0.6,
    height: Constants.heightOfBoxes * 0.6,
    alignSelf: 'center',
    marginTop: '5%',
  }, 
  carDisplay: {
    height: Constants.heightOfBoxes,
    backgroundColor: '#FFFFFF'
  }
});