import React from 'react';
import { WithContext as ReactTags } from 'react-tag-input';

const KeyCodes = {
  comma: 188,
  enter: 13
};

const delimiters = [KeyCodes.comma, KeyCodes.enter];
export const GenreTagSelector = (props) => {
    const [tags, setTags] = React.useState([]);
    const onUpdate = props.onUpdate;
    const genre_tags = Array.from(props.genre_tags);
    const suggestions = genre_tags.map(genre => {
        return {
            id: genre,
            text: genre
        };
    });

    const handleDelete = i => {
        const updatedTags = tags.filter((tag, index) => index !== i)
        setTags(updatedTags);
        onUpdate(updatedTags.map(suggestion => suggestion.text));
    };

    const handleAddition = tag => {
        const updatedTags = [...tags, tag];
        setTags(updatedTags);
        onUpdate(updatedTags.map(suggestion => suggestion.text));
    };

    return (
        <div className="App">
            <div>
                <ReactTags
                    tags={tags}
                    suggestions={suggestions}
                    delimiters={delimiters}
                    handleDelete={handleDelete}
                    handleAddition={handleAddition}
                    inputFieldPosition="inline"
                    placeholder="Genre tags..."
                    minQueryLength={0}
                    allowDragDrop={false}
                    inline
                    autofocus={false}
                    autocomplete />
            </div>
        </div>
    );
};
