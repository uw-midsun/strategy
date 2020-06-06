/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */

import React from 'react';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  StatusBar,
  Dimensions,
  FlatList,
} from 'react-native';
import {Header} from 'react-native-elements';

const data = [
  {id: "velocity", displayName: "Velocity", value: "10"},
  {id: "recommendedVelocity", displayName: "Recommended Velocity", value: "11"},
  {id: "elevation", displayName: "Elevation", value: "12"}
];
const numColumns = 2;
const sizeOfBoxes = Dimensions.get('window').width / numColumns * 0.75;
const heightOfPage = Dimensions.get('window').height;

const App: () => React$Node = () => {
  return (
    <>
      <StatusBar barStyle="dark-content" />
      <Header
        centerComponent={{text: "STRATEGY", style: {color: "#FFFFFF", fontSize: 20}}}
      />
      <SafeAreaView>
        <View style={styles.carDisplay}>
          <Text>Insert some graphic here</Text>
        </View>
        <FlatList
          data = {data}
          renderItem={({item}) => (
            <View style={styles.itemStyles}>
              <Text style={styles.item}>{item.value}{"\n"}{item.displayName}</Text>
            </View>
          )}
          keyExtractor={item => item.id}
          numColumns = {numColumns}
          style={styles.listStyles}
        />
      </SafeAreaView>
    </>
  );
};

const styles = StyleSheet.create({
  carDisplay: {
    height: heightOfPage / 5,
  },
  listStyles: {

  },
  itemStyles: {
    width: sizeOfBoxes,
    height: sizeOfBoxes,
  },
  item: {
    flex: 1,
    margin: 3,
    backgroundColor: "#FFFFFF",
    fontSize: 20,
    textAlign: "center",
    textAlignVertical: "center",
  }
});

export default App;
