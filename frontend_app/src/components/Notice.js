import React from 'react';
import PropTypes from 'prop-types';

const Notice = ({ data }) => {
    if (data.length === 0) {
        return (
            <p>Nothing to show</p>
        );
    }
    else {
        return (
            <h2>{data[0]}</h2>
        );
    }
};

Notice.propTypes = {
    data: PropTypes.string.isRequired
};

export default Notice;