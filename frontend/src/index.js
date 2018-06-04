import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import axios from 'axios';


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
      <Table rows={rows} />
    )
  }
}

// ========================================

ReactDOM.render(
  <Content />,
  document.getElementById('root')
);
