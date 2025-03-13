import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Areas = () => {
  const [areas, setAreas] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAreas = async () => {
      try {
        const res = await axios.get("http://localhost:5000/areas");
        setAreas(res.data);
      } catch (error) {
        console.error("Error fetching areas:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAreas();
  }, []);

  return (
    <div className="container">
      <h2>Areas</h2>
      <button className="back-button" onClick={() => navigate("/")}>Back to Home</button>
      {loading ? (
        <p>Loading areas...</p>
      ) : areas.length > 0 ? (
        <div className="cards">
          {areas.map((area) => (
            <div key={area.id} className="card">
              <h3>{area.city}</h3>
            </div>
          ))}
        </div>
      ) : (
        <p>No Areas found.</p>
      )}
    </div>
  );
};

export default Areas;
