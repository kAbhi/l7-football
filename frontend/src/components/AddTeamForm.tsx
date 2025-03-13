import { useState } from "react";
import axios from "axios";

const AddTeamForm = ({ onTeamAdded }) => {
  const [name, setName] = useState("");
  const [country, setCountry] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await axios.post("http://localhost:5000/teams", { name, country });
      onTeamAdded(); // Refresh team list
      setName("");
      setCountry("");
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
      <h3>Add New Team</h3>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Team Name" required />
        <input type="text" value={country} onChange={(e) => setCountry(e.target.value)} placeholder="Country" required />
        <button type="submit">Add Team</button>
      </form>
    </div>
  );
};

export default AddTeamForm;
