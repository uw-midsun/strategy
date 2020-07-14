import React from 'react';
import {View, Text, StyleSheet} from 'react-native';
import {LineChart} from 'react-native-chart-kit';
import * as Constants from '../constants';

export default class PastData extends React.Component {

    state = {
        labels: ["test1", "test2"],
        data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        lastUpdate: "",
        type: "velocity"
    }

    fetchCurrentData = async (time_in_mins) => {
        await fetch(Constants.BASE_URL + Constants.PAST_ENDPOINT + time_in_mins)
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
        this.focusListener = this.props.navigation.addListener('focus', async() => this.fetchCurrentData(60));
    }

    componentWillUnmount() {
        this.focusListener();
    }

    render() {
        return (
        <View style={styles.main}>
          <Text style={styles.text}>Past Data{"\n"}Last updated: {this.state.lastUpdate}</Text>
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
            style={styles.chartStyles}
            bezier={true}
          />
          <Text style={styles.text}>Hell{"\n"}More infohere</Text>
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
    }
});