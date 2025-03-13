import { useState, useEffect } from "react";
import axios from "axios";

const AddMatchForm = ({ onMatchAdded }) => {
  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");
  const [date, setDate] = useState("");
  const [location, setLocation] = useState("");
  const [teams, setTeams] = useState([]);
  const [locations, setLocations] = useState([]);
  const [searchTerm1, setSearchTerm1] = useState("");
  const [searchTerm2, setSearchTerm2] = useState("");
  const [error, setError] = useState("");

  // Fetch teams and locations for the dropdowns
  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const res = await axios.get("http://localhost:5000/teams");
        setTeams(res.data);
      } catch (error) {
        console.error("Error fetching teams:", error);
      }
    };

    const fetchLocations = async () => {
      try {
        const res = await axios.get("http://localhost:5000/areas");
        setLocations(res.data);
      } catch (error) {
        console.error("Error fetching locations:", error);
      }
    };

    fetchTeams();
    fetchLocations();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await axios.post("http://localhost:5000/matches", { team1, team2, date, location });
      onMatchAdded(); // Refresh match list
      setTeam1("");
      setTeam2("");
      setDate("");
      setLocation("");
    } catch (err) {
      if (err.response && err.response.status === 400) {
        setError(err.response.data.error); // Display validation error
      } else {
        setError("Something went wrong. Please try again.");
      }
    }
  };

  // Filter teams based on search term
  const filteredTeams1 = teams.filter((t) =>
    t.name.toLowerCase().includes(searchTerm1.toLowerCase())
  );

  const filteredTeams2 = teams.filter((t) =>
    t.name.toLowerCase().includes(searchTerm2.toLowerCase())
  );

  return (
    <div>
      <h3>Add New Match</h3>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        {/* Searchable Team 1 Dropdown */}
        <div className="dropdown-container">
          <input
            type="text"
            value={searchTerm1}
            onChange={(e) => setSearchTerm1(e.target.value)}
            placeholder="Search team 1..."
            className="search-box"
          />
          <select value={team1} onChange={(e) => setTeam1(e.target.value)} required>
            <option value="">Select Team 1</option>
            {filteredTeams1.map((team) => (
              <option key={team.id} value={team.name}>{team.name}</option>
            ))}
          </select>
        </div>

        {/* Searchable Team 2 Dropdown */}
        <div className="dropdown-container">
          <input
            type="text"
            value={searchTerm2}
            onChange={(e) => setSearchTerm2(e.target.value)}
            placeholder="Search team 2..."
            className="search-box"
          />
          <select value={team2} onChange={(e) => setTeam2(e.target.value)} required>
            <option value="">Select Team 2</option>
            {filteredTeams2.map((team) => (
              <option key={team.id} value={team.name}>{team.name}</option>
            ))}
          </select>
        </div>

        {/* Date Input */}
        <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />

        {/* Location Text Box */}
        <input type="text" value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Location" required />

        <button type="submit">Add Match</button>
      </form>
    </div>
  );
};

export default AddMatchForm;
