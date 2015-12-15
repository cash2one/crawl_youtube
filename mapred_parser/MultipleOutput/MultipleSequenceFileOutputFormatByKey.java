package com.custom;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.lib.MultipleSequenceFileOutputFormat;

public class MultipleSequenceFileOutputFormatByKey extends MultipleSequenceFileOutputFormat<Text, Text> {
  /**
   * Use they key as part of the path for the final output file.
   */
  @Override
  /*protected String generateFileNameForKeyValue(Text key, Text value, String leaf) {
    String valueString = key.toString();
    String[] valueString_arr = valueString.split("\t", 2);
	Path first = new Path(valueString_arr[1], leaf);
	return new Path(valueString_arr[0], first.toString()).toString();
  }*/
  protected String generateFileNameForKeyValue(Text key, Text value, String leaf) {
    String valueString = key.toString();
	return new Path(valueString, leaf).toString();
  }

  /**
   * When actually writing the data, discard the key since it is already in
   * the file path.
   */
  @Override
  protected Text generateActualKey(Text key, Text value) {
    String valueString = value.toString();
    String[] valueString_arr = valueString.split("\t", 2);
    return new Text(valueString_arr[0]);
  }

  @Override
  protected Text generateActualValue(Text key, Text value) {
    String valueString = value.toString();
    String[] valueString_arr = valueString.split("\t", 2);
    return new Text(valueString_arr[1]);
  }
}
