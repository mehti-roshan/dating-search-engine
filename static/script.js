const ESSAY_PROMPTS = {
  "essay0": "About me",
  "essay1": "What I'm doing with my life",
  "essay2": "Things I'm good at",
  "essay3": "What people first notice about me",
  "essay4": "Favorite books, movies, shows, music, and food",
  "essay5": "Things I couldn't live without",
  "essay6": "Things I spend time thinking about",
  "essay7": "What I do on a typical Friday night",
  "essay8": "Something personal about me",
  "essay9": "Who should message me",
};

const form = document.querySelector("#search-form");
const queryInput = document.querySelector("#query");
const searchButton = document.querySelector("#search-button");
const resultsContainer = document.querySelector("#results");
const resultCount = document.querySelector("#result-count");

let activeRequest = null;

async function searchProfiles(query, filters = {}, signal) {
  const response = await fetch("/api/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    signal,
    body: JSON.stringify({
      query,
      limit: 10,
      ...filters,
    }),
  });

  if (!response.ok) {
    let message = "Search failed. Please try again.";

    try {
      const error = await response.json();
      message = error.detail || message;
    } catch {
      // Keep the default error message.
    }

    throw new Error(message);
  }

  return response.json();
}

function getFilters() {
  const formData = new FormData(form);
  const filters = {};

  const textFields = [
    "sex",
    "orientation",
    "status",
    "location",
  ];

  const numericFields = [
    "min_age",
    "max_age",
    "min_height",
    "max_height",
  ];

  for (const field of textFields) {
    const value = formData.get(field)?.trim();

    if (value) {
      filters[field] = value;
    }
  }

  for (const field of numericFields) {
    const value = formData.get(field);

    if (value !== null && value.trim() !== "") {
      filters[field] = Number(value);
    }
  }

  return filters;
}

function showMessage(title, description) {
  resultsContainer.replaceChildren();

  const state = document.createElement("div");
  state.className = "empty-state";

  const heading = document.createElement("h3");
  heading.textContent = title;

  const paragraph = document.createElement("p");
  paragraph.textContent = description;

  state.append(heading, paragraph);
  resultsContainer.append(state);
}

function getProfileExcerpt(profile) {
  const essayFields = [
    "essay0",
    "essay1",
    "essay2",
    "essay3",
    "essay4",
    "essay5",
    "essay6",
    "essay7",
    "essay8",
    "essay9",
  ];

  for (const field of essayFields) {
    const value = profile[field];

    if (typeof value === "string" && value.trim()) {
      return value.trim();
    }
  }

  return "This profile doesn't contain a written introduction.";
}

function formatHeight(value) {
  if (value === undefined || value === null || value === "") {
    return null;
  }

  const inches = Number(value);

  if (!Number.isFinite(inches) || inches <= 0) {
    return null;
  }

  const feet = Math.floor(inches / 12);
  const remainingInches = Math.round(inches % 12);

  return `${feet}'${remainingInches}"`;
}

function createProfileCard(result) {
  const profile = result.profile ?? {};

  const card = document.createElement("article");
  card.className = "profile-card";

  // Helpers
  function getValue(value) {
    if (value === null || value === undefined) return "";
    return String(value).trim();
  }

  function formatLabel(value) {
    if (!value) return "";

    return value
      .replace(/_/g, " ")
      .replace(/\s+/g, " ")
      .replace(/\b\w/g, (char) => char.toUpperCase());
  }

  function formatGender(value) {
    const gender = getValue(value).toLowerCase();

    const genders = {
      f: "Female",
      m: "Male",
      woman: "Woman",
      man: "Man",
      nonbinary: "Non-binary",
    };

    return genders[gender] || (value ? formatLabel(value) : "");
  }

  function formatHeight(value) {
    if (value === null || value === undefined || value === "") {
      return "";
    }

    const inches = Number(value);

    if (!Number.isFinite(inches) || inches <= 0) {
      return "";
    }

    const totalHalfInches = Math.round(inches * 2);
    const feet = Math.floor(totalHalfInches / 24);
    const remainingHalfInches = totalHalfInches % 24;

    const wholeInches = Math.floor(remainingHalfInches / 2);
    const halfInch = remainingHalfInches % 2 ? "½" : "";

    return `${feet}′${wholeInches}${halfInch}″`;
  }

  // Header
  const header = document.createElement("div");
  header.className = "profile-card-header";

  const headingGroup = document.createElement("div");

  const name = document.createElement("h3");
  name.className = "profile-name";

  const age = getValue(profile.age);
  name.textContent = age ? `${age} years old` : "Profile";

  const meta = document.createElement("div");
  meta.className = "profile-meta";

  const metadata = [
    formatGender(profile.sex),
    getValue(profile.location),
    formatHeight(profile.height),
    formatLabel(profile.orientation),
    formatLabel(profile.status),
  ].filter(Boolean);

  meta.textContent = metadata.join(" · ");

  headingGroup.append(name, meta);
  header.append(headingGroup);

  // Vector similarity score
  if (typeof result.score === "number") {
    const score = document.createElement("span");
    score.className = "profile-score";
    score.textContent = `Score ${result.score.toFixed(3)}`;
    score.title =
      "Vector similarity score, not a compatibility percentage.";

    header.append(score);
  }

  card.append(header);

  // All non-empty essays
  const essaysContainer = document.createElement("div");
  essaysContainer.className = "profile-essays";

  for (const [field, prompt] of Object.entries(ESSAY_PROMPTS)) {
    const essay = getValue(profile[field]);

    if (!essay) continue;

    const section = document.createElement("section");
    section.className = "profile-essay";

    const title = document.createElement("h4");
    title.className = "profile-essay-title";
    title.textContent = prompt;

    const text = document.createElement("p");
    text.className = "profile-essay-text";
    text.textContent = essay;

    section.append(title, text);
    essaysContainer.append(section);
  }

  if (essaysContainer.childElementCount > 0) {
    card.append(essaysContainer);
  }

  // Other profile attributes
  const attributeLabels = {
    body_type: "Body type",
    diet: "Diet",
    drinks: "Drinking",
    drugs: "Drugs",
    education: "Education",
    ethnicity: "Ethnicity",
    income: "Income",
    job: "Occupation",
    last_online: "Last online",
    offspring: "Children",
    pets: "Pets",
    religion: "Religion",
    sign: "Astrological sign",
    smokes: "Smoking",
    speaks: "Languages",
  };

  const attributesContainer = document.createElement("section");
  attributesContainer.className = "profile-attributes";

  const attributesTitle = document.createElement("h4");
  attributesTitle.className = "profile-attributes-title";
  attributesTitle.textContent = "About this person";

  const attributesGrid = document.createElement("dl");
  attributesGrid.className = "profile-attributes-grid";

  for (const [field, label] of Object.entries(attributeLabels)) {
    let value = getValue(profile[field]);

    // The dataset uses -1 to indicate undisclosed income.
    if (field === "income" && value === "-1") {
      value = "";
    }

    if (!value) continue;

    // Normalize a few values for display.
    if (field === "last_online") {
      const match = value.match(
        /^(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})$/
      );

      if (match) {
        value = `${match[1]}-${match[2]}-${match[3]} ${match[4]}:${match[5]}`;
      }
    }

    const item = document.createElement("div");
    item.className = "profile-attribute";

    const term = document.createElement("dt");
    term.textContent = label;

    const description = document.createElement("dd");
    description.textContent = value;

    item.append(term, description);
    attributesGrid.append(item);
  }

  if (attributesGrid.childElementCount > 0) {
    attributesContainer.append(attributesTitle, attributesGrid);
    card.append(attributesContainer);
  }

  return card;
}

function renderResults(data) {
  const results = Array.isArray(data.data) ? data.data : [];

  resultsContainer.replaceChildren();

  resultCount.textContent =
    `${results.length} ${results.length === 1 ? "result" : "results"}`;

  if (results.length === 0) {
    showMessage(
      "No matches this time.",
      "Try a broader description or loosen a few filters."
    );
    return;
  }

  const fragment = document.createDocumentFragment();

  for (const result of results) {
    console.log(result);
    
    fragment.append(createProfileCard(result));
  }

  resultsContainer.append(fragment);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const query = queryInput.value.trim();

  if (!query) {
    queryInput.focus();
    return;
  }

  // Cancel any previous search that is still running.
  activeRequest?.abort();

  const controller = new AbortController();
  activeRequest = controller;

  searchButton.disabled = true;
  searchButton.innerHTML = "Searching...";

  resultCount.textContent = "Finding people...";
  showMessage(
    "Searching profiles...",
    "Looking for people who match your description."
  );

  try {
    const filters = getFilters();

    const data = await searchProfiles(
      query,
      filters,
      controller.signal
    );

    // Ignore responses from requests that are no longer active.
    if (activeRequest !== controller) {
      return;
    }

    renderResults(data);
  } catch (error) {
    if (error.name === "AbortError") {
      return;
    }

    console.error("Profile search failed:", error);

    if (activeRequest === controller) {
      resultCount.textContent = "Search failed";

      showMessage(
        "Something went wrong.",
        error.message || "Please try again in a moment."
      );
    }
  } finally {
    if (activeRequest === controller) {
      activeRequest = null;
      searchButton.disabled = false;
      searchButton.innerHTML = 'Find people <span aria-hidden="true">↗</span>';
    }
  }
});