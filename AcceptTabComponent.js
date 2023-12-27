import React from "react";
import IndivualStatus from "./IndivualStatus";
import { useSelector } from "react-redux";

const AcceptedTabComponent = ({ data }) => {
  const loader = useSelector((state) => state.Loading.loading);

  return (
    <>
      <section className="review">
        <div className="container">
          <div className="row py-3">
            {data.map((item) => {
              if (item.status != "Accepted") return null;
              return <IndivualStatus data={item} />;
            })}

            {!data.some((item) => item.status == "Accepted") && !loader ? (
              <>
                <div className="row">
                  <div className="col-md-12  text-center">
                    <p className="text-danger">No data found for accepted status</p>
                  </div>
                </div>
              </>
            ) : null}
          </div>
        </div>
      </section>
    </>
  );
};

export default AcceptedTabComponent;
