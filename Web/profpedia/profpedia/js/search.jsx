import React from 'react';

function ProfInfo(props) {
  return (
    <tr>
      <th scope="row">{props.rank}</th>
      <td>{props.profName}</td>
      <td>{props.homepage}</td>
    </tr>
  );
}
class Search extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      query: '',
      profs: [],
      hasResult: false,
      selectUniversity: 'Null',
      selectField: 'Null',
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleQuerySubmit = this.handleQuerySubmit.bind(this);
    this.handleUniversityChange = this.handleUniversityChange.bind(this);
    this.handleFieldChange = this.handleFieldChange.bind(this);
  }


  handleChange(event) {
    this.setState({ query: event.target.value });
  }
  handleQuerySubmit(event) {
    event.preventDefault();
    const url = `/api/v1/search/q=${this.state.query}`;
    fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
      },
      redirect: 'manual',
      referrer: 'no-referrer',
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({ showSummary: false });
        if (data) {
          this.setState({
            profs: data.profs,
            hasResult: true,
          });
        } else {
          this.setState({
            profs: [],
            hasResult: false,
          });
        }
      })
      .catch(error => console.log(error)); // eslint-disable-line no-console
  }

  handleUniversityChange(e) {
    this.setState({ selectUniversity: e.target.value });
  }
  handleFieldChange(e) {
    this.setState({ selectField: e.target.value });
  }

  render() {
    const profList = [];
    if (this.state.hasResult) {
      for (let i = 0; i < this.state.profs.length; i++) {
        const newProfInfo = this.state.profs[i];
        const newProfRow = <ProfInfo rank={i + 1} profName={newProfInfo.prof_name}homepage={newProfInfo.homepage} />;
        profList.push(newProfRow);
      }
    } else {
      const newProfRow = <ProfInfo rank={1} profName="No Result" homepage="No url" />;
      profList.push(newProfRow);
    }

    /*
    if (docs.length !== 0) {
      // eslint-disable-next-line no-plusplus
      for (let i = 0; i < docs.length; i++) {
        const newTitleStr = docs[i].title;
        titleArray.push(newTitle);
      }
    }

    let result = titleArray;
    if (this.state.showSummary) {
      const similarDocsTitles = [];
      for (let i = 0; i < this.state.similarDocs.length; i++) {
        const newDocTitle = <div><p className="doc_title"> {this.state.similarDocs[i].title} </p></div>;
        similarDocsTitles.push(newDocTitle);
      }
      result = (<div>
        <p className="doc_summary" >{this.state.summary} </p>
        {similarDocsTitles}
      </div>);
    }
    */


    return (
      <div>
        <form onSubmit={this.handleQuerySubmit} >
          <div>
            <div className="md-form active-pink active-pink-2 mb-3 mt-0">
              <input className="form-control" type="text" placeholder="Search" aria-label="Enter your interests" value={this.state.query} onChange={this.handleChange} /> </div>
          </div>

          Select a university that you are interested in
          <div>
            <select
              value={this.state.selectUniversity}
              onChange={this.handleUniversityChange}
            >
              <option value="Null">Null</option>
              <option value="Michigan">Michigan</option>
              <option value="CMU">CMU</option>
            </select>
          </div>

          Select a field that you are interested in
          <div>
            <select
              value={this.state.selectField}
              onChange={this.handleFieldChange}
            >
              <option value="Null">Null</option>
              <option value="Word Embedding">Word Embedding</option>
              <option value="Word Embedding">Word Embedding</option>
            </select>
          </div>

          <div>
            <input type="submit" value="Search" onClick={this.handleQuerySubmit} />
          </div>
        </form>

        <p>Your search query is {this.state.query}</p>
        <p>Your selected university is {this.state.selectUniversity}</p>
        <p>Your selected field is {this.state.selectField}</p>
        <table className="table table-dark">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Professor Name</th>
              <th scope="col">Homepage</th>
            </tr>
          </thead>
          <tbody>
            {profList}
          </tbody>
        </table>
      </div>
    );
  }
}


export default Search;
