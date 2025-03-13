import { useState } from "react";
import axios from "axios";

const AddPlayerForm = ({ onPlayerAdded }) => {
  const [name, setName] = useState("");
  const [team, setTeam] = useState("");
  const [position, setPosition] = useState("");
  const [error, setError] = useState("");

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
        setError(err.response.data.error); // Display duplicate error
      } else {
        setError("Something went wrong. Please try again.");
      }
    }
  };

  return (
    <div>
      <h3>Add New Player</h3>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Player Name" required />
        <input type="text" value={team} onChange={(e) => setTeam(e.target.value)} placeholder="Team" required />
        <input type="text" value={position} onChange={(e) => setPosition(e.target.value)} placeholder="Position" required />
        <button type="submit">Add Player</button>
      </form>
    </div>
  );
};

export default AddPlayerForm;
