# Mairi's (very messy) notes
[FiveThirtyEight polling average methodology](https://fivethirtyeight.com/methodology/how-our-polling-averages-work/) - guideline for us?

- polls of likely voters > polls of registered voters > polls of all adults
- cap sample sizes at 5000, windsorize (idk if windsorizing makes sense here)
- if sample size isn't reported, use median sample size of polls from that polster of that type (if no other info, use median sample size of all other polls of that type) - note type doesn't matter for us
- for overlapping polls from a given firm -  dynamically remove polls with overlapping dates until greatest number of polls with no overlapping dates is retained (no)
- sample size weighting - square root of poll's sample size / square root for median sample size for group

[Pollster Rating Calculation](https://fivethirtyeight.com/features/how-fivethirtyeight-calculates-pollster-ratings/)
- grade corresponds to predictive plus-minus

# Ideas
- augment dataset with electoral college points?
- [how electoral college works](https://chatgpt.com/share/66e84bb5-ca58-8006-99ad-7697cf58228d)

# 1 Oct - Draft Report

## Introduction
Hillary Clinton's loss to Donald Trump in the 2016 American presidential election was as unexpected as it was humiliating. How did a former senator, first lady, and secretary of state[^1] lose to a washed-up reality TV star who, just a month before the election, made headlines for a resurfaced video in which he bragged about sexual assault[^2]?

Clinton has attributed much of the blame for her defeat to former FBI Director James Comey[^1]. On October 28, 2016, Comey sent a letter to Congress outlining the FBI's decision to reopen an investigation into Clinton's use of a private email server[^3]. The ensuing media circus dominated the news cycle during the final stretch of the campaign. Two days before the election, on November 6th, Comey announced that the new evidence did not warrant reopening the investigation after all[^4].

Given how things turned out, it's understandable that Clinton feels Comey sabotaged her. This investigation will explore whether there is evidence for the existence of "the Comey effect". It will also provide a comprehensive overview of polling methodology and the American electoral system. Readers are invited to consider ethical questions about the role of government officials and the media in ensuring free and fair elections.

## Graph

Below is an exploration of aggregated raw polling data, along with a moving average, for national polls and several swing states. These states had some of the closest margins in the country; while Clinton was predicted to win most of them, Trump ultimately secured victories across the board[^5]. It is worth noting that all of these states voted for Barack Obama in 2012[^6] and Joe Biden in 2020[^7]. A noticeable drop in the polls' moving average after October 31st is evident in the national polls and in all the listed states except Wisconsin.

Here, we have a direct comparison of the weighted average polls from Florida, Michigan, and Pensylvania. In all cases, there is a noticeable increase after the first presidential debate, and a decrease after Comey's letter. In terms of electoral college votes, Florida alone would've been sufficient for Clinton to win. This is not a new phenomenon; in 2000, 537 Florida votes decided George Bush's victory over Al Gore[^8].

## Conclusion

In his memoir, James Comey said that he was "sure Clinton would win"[^9]. If there is one thing that should be take away from this investigation, it is that election results are not guaranteed until the votes have been counted. Polls are not a crystal ball, particularily in the context of the American electoral college. It would be misleading to point to the Comey letter as the sole determiner of the election outcome, but there is some evidence that it did have at the very least a moderate impact. With the 2024 presedential election right around the corner, we implore government officals and media organizations to exercise care in their disclosure and coverage of stories that could influence the electorate.

[^1]: ["What Happened" by Hillary Rodham Clinton](https://books.google.ca/books/about/What_Happened.html?id=UjAIDgAAQBAJ&redir_esc=y)

[^2]: [Trump recorded having extremely lewd conversation about women in 2005](https://www.washingtonpost.com/politics/trump-recorded-having-extremely-lewd-conversation-about-women-in-2005/2016/10/07/3b9ce776-8cb4-11e6-bf8a-3d26847eeed4_story.html)

[^3]: [Letter to Congress From F.B.I. Director on Clinton Email Case](https://www.nytimes.com/interactive/2016/10/28/us/politics/fbi-letter.html)

[^4]: [Emails Warrant No New Action Against Hillary Clinton, F.B.I. Director Says](https://www.nytimes.com/2016/11/07/us/politics/hilary-clinton-male-voters-donald-trump.html)

[^5]: https://www.nytimes.com/elections/2016/results/president

[^6]: https://www.nytimes.com/elections/2012/results/president.html

[^7]: https://www.nytimes.com/interactive/2020/11/03/us/elections/results-president.html

[^8]: [The Florida Recount Of 2000: A Nightmare That Goes On Haunting](https://www.npr.org/2018/11/12/666812854/the-florida-recount-of-2000-a-nightmare-that-goes-on-haunting)

[^9]: ["A Higher Loyalty: Truth, Lies, and Leadership" by James Comey](https://books.google.ca/books/about/A_Higher_Loyalty.html?id=4CovDwAAQBAJ&redir_esc=y)



