import {Dimensions} from 'react-native';

export const numColumns = 1;
export const widthOfBoxes = Dimensions.get('window').width * 0.85;
export const heightOfPage = Dimensions.get('window').height;
export const heightOfBoxes = heightOfPage / 8;

export const BASE_URL = "http://10.0.2.2:5000/"; 
export const CURRENT_ENDPOINT = "current";
export const PAST_ENDPOINT = "previous/";

export const graphTypes = ["velocity", "elevation"];