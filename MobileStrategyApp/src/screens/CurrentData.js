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

const data = [
  {id: "velocity", displayName: "Velocity (km/h)", value: 10},
  {id: "recommendedVelocity", displayName: "Recommended Velocity (km/h)", value: 11},
  {id: "elevation", displayName: "Elevation (km)", value: 12}
];

//api_form = {
//   "elevation": 2.33051380781163e+17, 
//   "entry_time": "2020-06-20T17:43:22.981400", 
//   "recommended_velocity": -39.8884, 
//   "velocity": 17.096
// }
const numColumns = 1;
// const sizeOfBoxes = Dimensions.get('window').width / numColumns * 0.75;
const widthOfBoxes = Dimensions.get('window').width * 0.85;
const heightOfPage = Dimensions.get('window').height;
const heightOfBoxes = heightOfPage / 8;

const URL_ENDPOINT = "http://10.0.2.2:5000/current"; 


export default class CurrentData extends React.Component {
  state = {
    carData: []
  }

  async componentDidMount() {
    setInterval(async () => {
      fetch(URL_ENDPOINT)
      .then(res => res.json())
      .then(data => {
        console.log("ok");
        usable_form = [];
        for (ele in data) 
          usable_form.push({"id": ele, "value": data[ele]});
    
        this.setState({carData: usable_form});
      })
      .catch((error) => {
        console.log(`Something went wrong... ${error}`);
        this.setState({carData: data});

      });
    }, 3000);
  }

  render() {
    return (
      <>
        {/* <StatusBar barStyle="dark-content" /> */}
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
            style={styles.listStyle}
          />
        </SafeAreaView>
      </>
    );
  }
  
};
  
  
const styles = StyleSheet.create({
  headerColour: {
    backgroundColor:'#FFFFFF',
  },
  carDisplay: {
    height: heightOfPage / 5,
  },
  listStyle: {
    alignSelf: "center",
  },
  itemStyles: {
    width: widthOfBoxes,
    height: heightOfBoxes,
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