export function createElement(type, attributes) {
  const element = document.createElement(type);
  console.log({ attributes });

  if (attributes.innerText) {
    element.innerText = attributes.innerText;
  }

  if (attributes.innerHTML) {
    element.innerHTML = attributes.innerHTML ?? "";
  }

  element.style = {
    ...element.style,
    ...(attributes.style || {}),
  };

  if (attributes.classes) {
    attributes.classes.forEach((className) => {
      element.classList.add(className);
    });
  }

  if (attributes.children) {
    attributes.children.forEach((child) => {
      element.appendChild(child);
    });
  }

  return element;
}

export function updateScoreList(message) {
  const scoresList = document.getElementById(`scores_${message.board_id}`);

  const updatedScoresElements = message.updated_scores.map((score) => {
    const score_span = createElement("span", {
      innerText: score.value + " ",
    });
    const username = createElement("span", { innerText: score.username });
    const div = createElement("div", { children: [score_span, username] });

    return div;
  });

  scoresList.replaceChildren(...updatedScoresElements);
}
