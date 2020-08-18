import React from 'react';
import {View, Text, StyleSheet, Button} from 'react-native';
import {LineChart} from 'react-native-chart-kit';
import * as Constants from '../constants';
import DropDownPicker from 'react-native-dropdown-picker';
import Icon from 'react-native-vector-icons/Feather';

var minuteOptions = [];
for (var i = 0; i < 1000; i++) {
    minuteOptions.push({label: toString(i), value: toString(i), icon: () => <Icon name="flag" size={18} color="#900"/>});
}


export default class PastData extends React.Component {

    state = {
        labels: ["test1", "test2"],
        data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        lastUpdate: "",
        type: "velocity",
        time_in_mins: "60"
    }

    fetchGraphData = async () => {
        await fetch(Constants.BASE_URL + Constants.PAST_ENDPOINT + this.state.time_in_mins)
        .then(res => res.json())
        .then(data => {
            var newLabels = [], newData = [];
            for (var i = 0; i < data.length; i++) {
                if (i % (data.length / 4) == 0)
                    newLabels.push(data[i]["entry_time"].split('T')[1].split('.')[0]);
                
                newData.push(data[i][this.state.type]);
            }
            let updatedTime = data.length != 0 ? data[data.length - 1]["entry_time"].split('T').join(' ').split('.')[0] : "Error in call";
    
            this.setState({labels: newLabels, data: newData, lastUpdate: updatedTime});
        })
        .catch((error) => {
            console.log(`Something went wrong... ${error}`);
        });
    }

    async componentDidMount() {
        this.focusListener = this.props.navigation.addListener('focus', async() => this.fetchGraphData());
    }

    componentWillUnmount() {
        this.focusListener();
    }

    render() {
        return (
        <View style={styles.main}>
          <Text style={styles.text}>Past Data: Previous {this.state.time_in_mins} minutes{"\n"}Last updated: {this.state.lastUpdate}</Text>
          <LineChart
            data = {{
                labels: this.state.labels, 
                datasets: [{data: this.state.data}]
            }}
            width = {Constants.widthOfBoxes}
            height = {Constants.heightOfPage / 2}
            // yAxisLabel = {this.state.type}
            // yAxisInterval = 
            verticalLabelRotation={-20}
            withInnerLines = {false}
            chartConfig={{
                backgroundColor: "#000000",
                backgroundGradientFrom: "#ffffff",
                backgroundGradientTo: "#ffffff",
                decimalPlaces: 2, // optional, defaults to 2dp
                color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                style: {
                  borderRadius: 20
                },
                propsForDots: {
                  r: "1",
                  strokeWidth: "1",
                  stroke: "#000000"
                }
            }}
            backgroundColor="transparent"
            style={styles.chartStyles}
            bezier={true}
          />
          <View style={styles.bottomSection}>
            <DropDownPicker
                items={minuteOptions}

                defaultValue={toString(this.state.time_in_mins)}
                containerStyle={{height: 40}}
                style={{backgroundColor: "#fafafa"}}
                itemStyle={{justifyContent: "flex-start"}}
                dropDownStyle={{backgroundColor: "#fafafa"}}

                searchable={true}
                searchablePlaceholder="Search for an item"
                searchablePlaceholderTextColor="gray"
                seachableStyle={{}}
                searchableError={() => <Text>Not Found</Text>}

                onChangeItem={item => this.setState({time_in_mins: item.value})}
            />
            {/* <Button onPress={this.fetchGraphData} title={"Update"} color="#2A2F41"/> */}
          </View>
          
        </View>
      );
    } 
}

const styles = StyleSheet.create({
    main: {
        flex: 1,
        justifyContent: 'center', 
        alignItems: 'center' 
    },
    text: {
        flex: 1,
        margin: 3,
        fontSize: 16,
        textAlign: "center",
        textAlignVertical: "center",
    },
    chartStyles: {
        borderRadius: 10,
    },
    bottomSection: {
        flex: 1
    }
});