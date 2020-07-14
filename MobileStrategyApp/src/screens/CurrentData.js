import React from 'react';
import {
  SafeAreaView,
  StyleSheet,
  View,
  Text,
  FlatList,
} from 'react-native';
import * as Constants from '../constants';


export default class CurrentData extends React.Component {
  state = {
    carData: [],
    lastUpdate: "",
  }

  fetchCurrentData = async () => {
    await fetch(Constants.BASE_URL + Constants.CURRENT_ENDPOINT)
    .then(res => res.json())
    .then(data => {
      console.log("ok");
      
      // format: 2020-07-11T22:19:46.880119
      let timeStamp = data["entry_time"].split('T').join(' ').split('.')[0];
      delete data["entry_time"];

      usable_form = [];
      for (ele in data) 
        usable_form.push({"id": ele.split('_').join(' '), "value": data[ele]});
  
      this.setState({lastUpdate: timeStamp, carData: usable_form});
    })
    .catch((error) => {
      console.log(`Something went wrong... ${error}`);
      this.setState({lastUpdate: "error", carData: [{id:"Fetch", value: "error"}]});
    });
  }

  async componentDidMount() {
    var timer;
    console.log('mount');
    this.focusListener = this.props.navigation.addListener('focus', async () => {
      this.fetchCurrentData();
      timer = setInterval(() => this.fetchCurrentData(), 3000);
    });
    this.blurListener = this.props.navigation.addListener('blur', () => clearInterval(timer));
  }

  componentWillUnmount() {
    console.log('unmount');
    this.focusListener();
    this.blurListener();
  }

  render() {
    return (
      <>
        <SafeAreaView>
          <FlatList
            data = {this.state.carData}
            renderItem={({item}) => (
              <View style={styles.itemStyles}>
                <Text style={styles.item}>{item.id}{": "}{item.value}</Text>
              </View>
            )}
            keyExtractor={item => item.id}
            numColumns = {Constants.numColumns}
            style={styles.listStyle}
          />
          <View style={styles.itemStyles}>
            <Text style={styles.bottomText}>Last updated: {this.state.lastUpdate}</Text>
          </View>
        </SafeAreaView>
      </>
    );
  }
  
};
  
  
const styles = StyleSheet.create({
  headerColour: {
    backgroundColor:'#FFFFFF',
  },
  imageStyling: {
    width: Constants.widthOfBoxes,
    height: Constants.heightOfBoxes,
    alignSelf: 'center',
  },
  carDisplay: {
    height: Constants.heightOfPage / 5,
  },
  listStyle: {
    alignSelf: "center",
    marginTop: '10%',
  },
  itemStyles: {
    width: Constants.widthOfBoxes,
    height: Constants.heightOfBoxes,
  },
  item: {
    flex: 1,
    margin: 3,
    backgroundColor: "#2A2F41",
    color: "#FFFFFF",
    fontSize: 20,
    textAlign: "center",
    textAlignVertical: "center",
  }, 
  bottomText: {
    flex: 1,
    margin: 3,
    fontSize: 16,
    textAlign: "center",
    textAlignVertical: "center",
  }
});