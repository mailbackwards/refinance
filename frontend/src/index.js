import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import C3Chart from 'react-c3js';
import 'c3/c3.css';
import './index.css';

const data = {
  columns: [
    ['data1', 30, 200, 100, 400, 150, 250],
    ['data2', 50, 20, 10, 40, 15, 25]
  ]
}


class Row extends React.Component {
  render() {
    let dataPoints = this.props.values.map((value, index) =>
      <td key={index}>{value}</td>
    )
    return (
      <tr>
        {dataPoints}
      </tr>
    )
  }
}


class Table extends React.Component {
  render() {
    let rowList = this.props.rows.map((row, index) =>
      <Row key={index} values={row} />
    )
    return (
      <table>
        <tbody>
          {rowList}
        </tbody>
      </table>
    );
  }
}


class Content extends React.Component {
  constructor(props) {
    super(props);
    this.state = {rows: []}
  }

  updateRows(newRows) {
    this.setState({rows: newRows});
  }

  componentDidMount() {
    var self = this;
    axios.get('http://localhost:8000/api/transactions/')
      .then(function (response) {
        let newRows = response.data.map((row) =>
          [row.amount, row.description, row.posted_date]
        );
        self.updateRows(newRows);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  render() {
    const rows = this.state.rows
    return (
      <div>
        <C3Chart data={data} />
        <Table rows={rows} />
      </div>
    )
  }
}

// ========================================

ReactDOM.render(
  <Content />,
  document.getElementById('root')
);
