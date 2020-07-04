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

// const data = [
//   {id: "velocity", displayName: "Velocity (km/h)", value: 10},
//   {id: "recommendedVelocity", displayName: "Recommended Velocity (km/h)", value: 11},
//   {id: "elevation", displayName: "Elevation (km)", value: 12}
// ];

//api_form = {
//   "elevation": 2.33051380781163e+17, 
//   "entry_time": "2020-06-20T17:43:22.981400", 
//   "recommended_velocity": -39.8884, 
//   "velocity": 17.096
// }
const numColumns = 2;
const sizeOfBoxes = Dimensions.get('window').width / numColumns * 0.75;
const heightOfPage = Dimensions.get('window').height;
const STRATEGY_ENDPOINT = "http://10.0.2.2:5000/mobile"; 

export default class App extends React.Component {
  state = {
    carData: []
  }

  async componentDidMount() {
    setInterval(async () => {
      fetch(STRATEGY_ENDPOINT)
      .then(res => res.json())
      .then(data => {
        //transform array somehow into form we want
        usable_form = [];
        for (ele in data) {
            current = {};
            current["id"] = ele;
            current["value"] = data[ele];

            usable_form.push(current);
        }

        console.log(usable_form);

        this.setState((state) => {
          return {carData: usable_form};
        });
      })
      .catch((error) => {
        console.log(`Something went wrong... ${error}`);
      });
    }, 3000);
  }

  render() {
    return (
      <>
        <StatusBar barStyle="dark-content" />
        <Header
          centerComponent={{text: "STRATEGY", style: {color: "#FFFFFF", fontSize: 18}}}
        />
        <SafeAreaView>
          <View style={styles.carDisplay}>
            <Text>Insert some graphic here</Text>
          </View>
          <FlatList
            data = {this.state.carData}
            renderItem={({item}) => (
              <View style={styles.itemStyles}>
                <Text style={styles.item}>{item.value}{"\n"}{item.id}</Text>
              </View>
            )}
            keyExtractor={item => item.id}
            numColumns = {numColumns}
            style={styles.listStyles}
          />
        </SafeAreaView>
      </>
    );
  }
  
};

const styles = StyleSheet.create({
  carDisplay: {
    height: heightOfPage / 5,
  },
  listStyles: {
    alignSelf: "center",
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
