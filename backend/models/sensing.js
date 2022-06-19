'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class sensing extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  };
  sensing.init({
    num1: DataTypes.DOUBLE,
    num2: DataTypes.DOUBLE,
    num3: DataTypes.DOUBLE
  }, {
    sequelize,
    modelName: 'sensing',
    tableName: 'sensing'
  });
  return sensing;
};