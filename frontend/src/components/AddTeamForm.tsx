import { useState } from "react";
import axios from "axios";

const AddTeamForm = ({ onTeamAdded }: { onTeamAdded: () => void }) => {
  const [name, setName] = useState("");
  const [country, setCountry] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await axios.post("http://localhost:5000/teams", { name, country });
    onTeamAdded();
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Name" value={name} onChange={e => setName(e.target.value)} required />
      <input type="text" placeholder="Country" value={country} onChange={e => setCountry(e.target.value)} required />
      <button type="submit">Add Team</button>
    </form>
  );
};

export default AddTeamForm;
