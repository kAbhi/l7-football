import { useState, useEffect } from "react";
import axios from "axios";

const AddPlayerForm = ({ onPlayerAdded }) => {
  const [name, setName] = useState("");
  const [team, setTeam] = useState("");
  const [position, setPosition] = useState("");
  const [teams, setTeams] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [error, setError] = useState("");

  // Fetch teams for the dropdown
  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const res = await axios.get("http://localhost:5000/teams");
        setTeams(res.data);
      } catch (error) {
        console.error("Error fetching teams:", error);
      }
    };

    fetchTeams();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await axios.post("http://localhost:5000/players", { name, team, position });
      onPlayerAdded(); // Refresh player list
      setName("");
      setTeam("");
      setPosition("");
    } catch (err) {
      if (err.response && err.response.status === 400) {
        setError(err.response.data.error); // Display validation error
      } else {
        setError("Something went wrong. Please try again.");
      }
    }
  };

  // Filter teams based on search term
  const filteredTeams = teams.filter((t) =>
    t.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <h3>Add New Player</h3>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Player Name" required />

        {/* Searchable Team Dropdown */}
        <div className="dropdown-container">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search team..."
            className="search-box"
          />
          <select value={team} onChange={(e) => setTeam(e.target.value)} required>
            <option value="">Select a Team</option>
            {filteredTeams.map((team) => (
              <option key={team.id} value={team.name}>{team.name}</option>
            ))}
          </select>
        </div>

        <input type="text" value={position} onChange={(e) => setPosition(e.target.value)} placeholder="Position" required />
        <button type="submit">Add Player</button>
      </form>
    </div>
  );
};

export default AddPlayerForm;
