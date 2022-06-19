'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class command extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  };
  command.init({
    time: DataTypes.DATE,
    cmd_string: DataTypes.STRING,
    arg_string: DataTypes.STRING,
    is_finish: DataTypes.INTEGER
  }, {
    sequelize,
    modelName: 'command',
  });
  return command;
};